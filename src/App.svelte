<script lang="ts">
  import { loadMatches, calculateStats } from './lib/data';
  import type { Match, MatchStats } from './lib/types';
  import { onMount } from 'svelte';
  import { Trophy, Search, Flame, Calendar, ChevronDown, ChevronUp, TrendingUp, BarChart3, Shield, MapPin } from 'lucide-svelte';

  let matches: Match[] = $state([]);
  let loading = $state(true);
  let error = $state('');
  let activeTab = $state('all');
  let searchQuery = $state('');
  let yearFilter = $state('');
  let resultFilter = $state('');
  let expandedMatchId = $state<string | null>(null);
  let stats = $state<MatchStats | null>(null);

  const years = $derived(
    [...new Set(matches.map(m => m.year).filter(y => y !== null).sort((a, b) => b! - a!))] as number[]
  );

  const filteredMatches = $derived(
    matches.filter(match => {
      const matchesSearch = searchQuery === '' ||
        match.homeTeam.toLowerCase().includes(searchQuery.toLowerCase()) ||
        match.awayTeam.toLowerCase().includes(searchQuery.toLowerCase()) ||
        match.opponent.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (match.competition || '').toLowerCase().includes(searchQuery.toLowerCase());
      
      const matchesYear = yearFilter === '' || match.year?.toString() === yearFilter;
      const matchesResult = resultFilter === '' || match.result === resultFilter;
      
      return matchesSearch && matchesYear && matchesResult;
    })
  );

  const displayedMatches = $derived(
    activeTab === 'wins' ? filteredMatches.filter(m => m.result === 'W') :
    activeTab === 'losses' ? filteredMatches.filter(m => m.result === 'L') :
    activeTab === 'draws' ? filteredMatches.filter(m => m.result === 'D') :
    filteredMatches
  );

  const tabs = $derived([
    { id: 'all', label: 'Todos', count: filteredMatches.length, color: 'red' },
    { id: 'wins', label: 'Victorias', count: filteredMatches.filter(m => m.result === 'W').length, color: 'emerald' },
    { id: 'draws', label: 'Empates', count: filteredMatches.filter(m => m.result === 'D').length, color: 'amber' },
    { id: 'losses', label: 'Derrotas', count: filteredMatches.filter(m => m.result === 'L').length, color: 'red' }
  ]);

  onMount(async () => {
    try {
      matches = await loadMatches();
      stats = calculateStats(matches);
    } catch (e) {
      error = 'Error cargando los datos';
    } finally {
      loading = false;
    }
  });

  function getResultStyles(result: string) {
    switch (result) {
      case 'W': return { color: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/30', label: 'Victoria', badge: 'V' };
      case 'L': return { color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/30', label: 'Derrota', badge: 'D' };
      case 'D': return { color: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/30', label: 'Empate', badge: 'E' };
      default: return { color: 'text-gray-400', bg: 'bg-gray-500/10', border: 'border-gray-500/30', label: result, badge: '?' };
    }
  }

  function toggleMatch(id: string) {
    expandedMatchId = expandedMatchId === id ? null : id;
  }

  function formatDate(dateStr: string): string {
    if (!dateStr) return '-';
    const parts = dateStr.split('/');
    if (parts.length === 3) {
      const day = parts[0];
      const month = parts[1];
      const year = parts[2];
      const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
      return `${day} ${months[parseInt(month) - 1]} ${year}`;
    }
    return dateStr;
  }

  function getTeamLogoPlaceholder(team: string): string {
    return team.charAt(0).toUpperCase();
  }
</script>

<div class="min-h-screen bg-[#0a0a0a]">
  
  <header class="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0a]/95 backdrop-blur-md border-b border-white/5">
    <div class="max-w-6xl mx-auto px-6">
      <div class="flex items-center justify-between h-20">
        <div class="flex items-center gap-4">
          <div class="relative">
            <div class="absolute inset-0 bg-red-600 blur-xl opacity-40"></div>
            <div class="relative w-12 h-12 bg-gradient-to-br from-red-600 to-red-800 rounded-lg flex items-center justify-center shadow-2xl">
              <Flame class="w-7 h-7 text-white" strokeWidth={2.5} />
            </div>
          </div>
          
          <div class="flex flex-col">
            <h1 class="text-2xl font-black tracking-tight text-white">
              HISTORIA <span class="text-red-600">ROJA</span>
            </h1>
            <p class="text-xs text-white/40 font-medium tracking-widest uppercase">Club Atlético Independiente</p>
          </div>
        </div>

        {#if stats}
          <div class="hidden md:flex items-center gap-8">
            <div class="text-center">
              <p class="text-3xl font-black text-white">{stats.totalMatches}</p>
              <p class="text-[10px] text-white/40 uppercase tracking-wider">Partidos</p>
            </div>
            <div class="w-px h-10 bg-white/10"></div>
            <div class="text-center">
              <p class="text-3xl font-black text-emerald-400">{stats.wins}</p>
              <p class="text-[10px] text-white/40 uppercase tracking-wider">Victorias</p>
            </div>
            <div class="w-px h-10 bg-white/10"></div>
            <div class="text-center">
              <p class="text-3xl font-black text-red-500">{stats.losses}</p>
              <p class="text-[10px] text-white/40 uppercase tracking-wider">Derrotas</p>
            </div>
          </div>
        {/if}
      </div>
    </div>
  </header>

  <main class="pt-28 pb-20">
    <div class="max-w-6xl mx-auto px-6">
      
      {#if stats}
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-white/[0.08] to-white/[0.02] border border-white/10 p-5">
            <div class="absolute top-0 right-0 p-3">
              <BarChart3 class="w-5 h-5 text-white/20" />
            </div>
            <p class="text-4xl font-black text-white mb-1">{stats.totalMatches}</p>
            <p class="text-xs text-white/40 uppercase tracking-wider">Total Partidos</p>
            <div class="mt-3 flex gap-1">
              <div class="h-1 flex-1 rounded-full bg-emerald-500/30"></div>
              <div class="h-1 flex-1 rounded-full bg-amber-500/30"></div>
              <div class="h-1 flex-1 rounded-full bg-red-500/30"></div>
            </div>
          </div>

          <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-500/10 to-transparent border border-emerald-500/20 p-5">
            <div class="absolute top-0 right-0 p-3">
              <Trophy class="w-5 h-5 text-emerald-500/30" />
            </div>
            <p class="text-4xl font-black text-emerald-400 mb-1">{stats.wins}</p>
            <p class="text-xs text-white/40 uppercase tracking-wider">Victorias</p>
            <p class="text-xs text-emerald-400/60 mt-2">{((stats.wins / stats.totalMatches) * 100).toFixed(1)}%</p>
          </div>

          <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-amber-500/10 to-transparent border border-amber-500/20 p-5">
            <div class="absolute top-0 right-0 p-3">
              <TrendingUp class="w-5 h-5 text-amber-500/30" />
            </div>
            <p class="text-4xl font-black text-amber-400 mb-1">{stats.draws}</p>
            <p class="text-xs text-white/40 uppercase tracking-wider">Empates</p>
            <p class="text-xs text-amber-400/60 mt-2">{((stats.draws / stats.totalMatches) * 100).toFixed(1)}%</p>
          </div>

          <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-red-500/10 to-transparent border border-red-500/20 p-5">
            <div class="absolute top-0 right-0 p-3">
              <Shield class="w-5 h-5 text-red-500/30" />
            </div>
            <p class="text-4xl font-black text-red-400 mb-1">{stats.losses}</p>
            <p class="text-xs text-white/40 uppercase tracking-wider">Derrotas</p>
            <p class="text-xs text-red-400/60 mt-2">{((stats.losses / stats.totalMatches) * 100).toFixed(1)}%</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div class="rounded-2xl bg-gradient-to-br from-white/[0.05] to-transparent border border-white/10 p-5">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs text-white/40 uppercase tracking-wider">Goles a Favor</span>
              <span class="text-xs text-emerald-400">+{stats.goalsScored}</span>
            </div>
            <p class="text-3xl font-black text-white">{stats.goalsScored}</p>
            <p class="text-xs text-white/30 mt-1">{(stats.goalsScored / stats.totalMatches).toFixed(2)} promedio</p>
          </div>

          <div class="rounded-2xl bg-gradient-to-br from-white/[0.05] to-transparent border border-white/10 p-5">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs text-white/40 uppercase tracking-wider">Goles en Contra</span>
              <span class="text-xs text-red-400">-{stats.goalsConceded}</span>
            </div>
            <p class="text-3xl font-black text-white">{stats.goalsConceded}</p>
            <p class="text-xs text-white/30 mt-1">{(stats.goalsConceded / stats.totalMatches).toFixed(2)} promedio</p>
          </div>

          <div class="rounded-2xl bg-gradient-to-br from-red-500/10 to-transparent border border-red-500/20 p-5">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs text-white/40 uppercase tracking-wider">Diferencia</span>
              <span class="text-xs {stats.goalDifference >= 0 ? 'text-emerald-400' : 'text-red-400'}">
                {stats.goalDifference >= 0 ? '+' : ''}{stats.goalDifference}
              </span>
            </div>
            <p class="text-3xl font-black {stats.goalDifference >= 0 ? 'text-emerald-400' : 'text-red-400'}">
              {stats.goalDifference > 0 ? '+' : ''}{stats.goalDifference}
            </p>
            <p class="text-xs text-white/30 mt-1">Balance general</p>
          </div>
        </div>
      {/if}

      <div class="bg-white/[0.03] backdrop-blur-sm rounded-3xl border border-white/10 p-6 mb-6">
        <div class="flex flex-col lg:flex-row gap-4">
          <div class="relative flex-1">
            <Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
            <input
              type="text"
              placeholder="Buscar equipo, torneo..."
              bind:value={searchQuery}
              class="w-full bg-black/40 border border-white/10 rounded-2xl pl-12 pr-4 py-4 text-white placeholder:text-white/30 focus:outline-none focus:border-red-500/50 transition-all"
            />
          </div>
          
          <div class="flex gap-3">
            <select
              bind:value={yearFilter}
              class="bg-black/40 border border-white/10 rounded-2xl px-4 py-4 text-white focus:outline-none focus:border-red-500/50 transition-all min-w-[140px]"
            >
              <option value="">Todos los años</option>
              {#each years as year}
                <option value={year.toString()}>{year}</option>
              {/each}
            </select>
            
            <select
              bind:value={resultFilter}
              class="bg-black/40 border border-white/10 rounded-2xl px-4 py-4 text-white focus:outline-none focus:border-red-500/50 transition-all min-w-[160px]"
            >
              <option value="">Todos los resultados</option>
              <option value="W">Victorias</option>
              <option value="L">Derrotas</option>
              <option value="D">Empates</option>
            </select>
          </div>
        </div>

        <div class="flex gap-2 mt-6 pt-6 border-t border-white/10 overflow-x-auto">
          {#each tabs as tab}
            <button
              class="px-5 py-2.5 rounded-xl text-sm font-semibold transition-all whitespace-nowrap {activeTab === tab.id ? `bg-${tab.color}-600 text-white` : 'bg-white/5 text-white/50 hover:bg-white/10 hover:text-white'}"
              onclick={() => activeTab = tab.id}
            >
              {tab.label}
              <span class="ml-2 px-2 py-0.5 rounded-full text-xs {activeTab === tab.id ? 'bg-white/20' : 'bg-white/10'}">
                {tab.count}
              </span>
            </button>
          {/each}
        </div>
      </div>

      {#if loading}
        <div class="flex items-center justify-center py-20">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 border-2 border-red-600 border-t-transparent rounded-full animate-spin"></div>
            <span class="text-white/40 text-lg">Cargando historial...</span>
          </div>
        </div>
      {:else if error}
        <div class="text-center py-20">
          <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-red-500/10 flex items-center justify-center">
            <Shield class="w-8 h-8 text-red-500" />
          </div>
          <p class="text-white/40 text-lg">{error}</p>
        </div>
      {:else if displayedMatches.length === 0}
        <div class="text-center py-20">
          <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-white/5 flex items-center justify-center">
            <Search class="w-8 h-8 text-white/20" />
          </div>
          <p class="text-white/40 text-lg">No se encontraron partidos</p>
          <p class="text-white/20 text-sm mt-2">Intenta con otros filtros</p>
        </div>
      {:else}
        <div class="space-y-3">
          {#each displayedMatches as match (match.id)}
            {@const resultStyle = getResultStyles(match.result)}
            {@const isExpanded = expandedMatchId === match.id}
            
            <button
              class="w-full text-left group"
              onclick={() => toggleMatch(match.id)}
            >
              <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-white/[0.06] to-white/[0.02] border border-white/10 transition-all duration-300 hover:border-white/20 hover:from-white/[0.08] {isExpanded ? 'border-white/20' : ''}"
              >
                
                <div class="absolute left-0 top-0 bottom-0 w-1 {resultStyle.bg}"></div>
                
                <div class="p-5 pl-6">
                  <div class="flex items-center gap-4">
                    
                    <div class="flex-shrink-0 w-16 text-center">
                      <div class="w-10 h-10 mx-auto rounded-xl {resultStyle.bg} border {resultStyle.border} flex items-center justify-center mb-1">
                        <span class="text-lg font-black {resultStyle.color}">{resultStyle.badge}</span>
                      </div>
                      <p class="text-[10px] font-medium text-white/40 uppercase">{resultStyle.label}</p>
                    </div>

                    <div class="flex-1">
                      <div class="flex items-center gap-3 mb-3">
                        <span class="flex items-center gap-1.5 text-xs text-white/40">
                          <Calendar class="w-3.5 h-3.5" />
                          {formatDate(match.date)}
                        </span>
                        
                        {#if match.year}
                          <span class="px-2 py-0.5 rounded-full bg-white/10 text-[10px] font-medium text-white/50">
                            {match.year}
                          </span>
                        {/if}
                        
                        <span class="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-white/5 text-[10px] font-medium text-white/50">
                          <MapPin class="w-3 h-3" />
                          {match.isHome ? 'Local' : 'Visitante'}
                        </span>
                      </div>
                      
                      <div class="flex items-center justify-center gap-6">
                        <div class="flex-1 text-right">
                          <p class="text-base font-bold text-white/90">{match.homeTeam}</p>
                          {#if match.isHome}
                            <span class="inline-flex items-center gap-1 text-[10px] text-red-400/60 mt-0.5">
                              <span class="w-1 h-1 rounded-full bg-red-500"></span>
                              Local
                            </span>
                          {/if}
                        </div>
                        
                        <div class="flex items-center gap-3 px-5 py-2.5 bg-black/40 rounded-xl border border-white/10">
                          <span class="text-2xl font-black text-white">{match.homeGoals}</span>
                          <span class="text-white/20 font-light">-</span>
                          <span class="text-2xl font-black text-white">{match.awayGoals}</span>
                        </div>
                        
                        <div class="flex-1 text-left">
                          <p class="text-base font-bold text-white/90">{match.awayTeam}</p>
                          {#if !match.isHome}
                            <span class="inline-flex items-center gap-1 text-[10px] text-red-400/60 mt-0.5">
                              <span class="w-1 h-1 rounded-full bg-red-500"></span>
                              Visitante
                            </span>
                          {/if}
                        </div>
                      </div>
                      
                      {#if match.competition}
                        <div class="mt-3 text-center">
                          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 text-[11px] text-white/40">
                            <Trophy class="w-3 h-3" />
                            {match.competition}
                          </span>
                        </div>
                      {/if}
                    </div>

                    <div class="flex-shrink-0">
                      {#if isExpanded}
                        <ChevronUp class="w-5 h-5 text-white/40" />
                      {:else}
                        <ChevronDown class="w-5 h-5 text-white/20 group-hover:text-white/40 transition-colors" />
                      {/if}
                    </div>
                  </div>

                  {#if isExpanded}
                    <div class="mt-5 pt-5 border-t border-white/10">
                      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div class="bg-white/[0.03] rounded-xl p-4">
                          <p class="text-[10px] text-white/30 uppercase tracking-wider mb-1">Competición</p>
                          <p class="text-sm font-medium text-white/80">{match.competition || 'Primera División'}</p>
                        </div>
                        
                        <div class="bg-white/[0.03] rounded-xl p-4">
                          <p class="text-[10px] text-white/30 uppercase tracking-wider mb-1">Ubicación</p>
                          <p class="text-sm font-medium text-white/80">{match.isHome ? 'Estadio Libertadores de América' : 'Estadio Visitante'}</p>
                        </div>
                        
                        <div class="bg-white/[0.03] rounded-xl p-4">
                          <p class="text-[10px] text-white/30 uppercase tracking-wider mb-1">Rival</p>
                          <p class="text-sm font-medium text-white/80">{match.opponent}</p>
                        </div>
                        
                        <div class="bg-white/[0.03] rounded-xl p-4">
                          <p class="text-[10px] text-white/30 uppercase tracking-wider mb-1">Diferencia de Goles</p>
                          <p class="text-sm font-medium {match.result === 'W' ? 'text-emerald-400' : match.result === 'L' ? 'text-red-400' : 'text-amber-400'}">
                            {match.isHome 
                              ? match.homeGoals - match.awayGoals 
                              : match.awayGoals - match.homeGoals}
                          </p>
                        </div>
                      </div>
                    </div>
                  {/if}
                </div>
              </div>
            </button>
          {/each}
        </div>
      {/if}
    </div>
  </main>

  <footer class="border-t border-white/5 bg-black/30">
    <div class="max-w-6xl mx-auto px-6 py-8">
      <div class="flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-red-600 rounded-lg flex items-center justify-center">
            <Flame class="w-4 h-4 text-white" />
          </div>
          <span class="text-sm text-white/40">Historia Roja © 2025</span>
        </div>
        
        <p class="text-sm text-white/20">El Orgullo Nacional — Club Atlético Independiente</p>
      </div>
    </div>
  </footer>
</div>
