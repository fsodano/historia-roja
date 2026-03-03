<script lang="ts">
  import { parseMatches, calculateStats, calculateTeamStats } from './lib/data';
  import type { Match, MatchStats } from './lib/types';
  import Button from './lib/components/ui/button.svelte';
  import Input from './lib/components/ui/input.svelte';
  import Select from './lib/components/ui/select.svelte';
  import Badge from './lib/components/ui/badge.svelte';
  import TabsTrigger from './lib/components/ui/tabs-trigger.svelte';
  import MatchCard from './lib/components/MatchCard.svelte';
  import StatsCard from './lib/components/StatsCard.svelte';
  import TeamStatsTable from './lib/components/TeamStatsTable.svelte';
  import { Trophy, Target, Swords, TrendingUp, Shield, Search, Filter, Flame, History } from 'lucide-svelte';

  const allMatches = parseMatches();
  const stats: MatchStats = calculateStats(allMatches);
  const teamStats = calculateTeamStats(allMatches);

  let searchQuery = $state('');
  let resultFilter = $state('');
  let locationFilter = $state('');
  let activeTab = $state('matches');
  let isMenuOpen = $state(false);

  const filteredMatches = $derived(
    allMatches.filter(match => {
      const matchesSearch = 
        match.homeTeam.toLowerCase().includes(searchQuery.toLowerCase()) ||
        match.awayTeam.toLowerCase().includes(searchQuery.toLowerCase()) ||
        match.opponent.toLowerCase().includes(searchQuery.toLowerCase());
      
      const matchesResult = !resultFilter || match.result === resultFilter;
      const matchesLocation = !locationFilter || 
        (locationFilter === 'home' && match.isHome) ||
        (locationFilter === 'away' && !match.isHome);

      return matchesSearch && matchesResult && matchesLocation;
    })
  );

  const recentMatches = $derived(filteredMatches.slice(0, 10));
  const biggestWins = $derived(
    [...filteredMatches]
      .filter(m => m.result === 'W')
      .sort((a, b) => {
        const diffA = Math.abs((a.isHome ? a.homeGoals : a.awayGoals) - (a.isHome ? a.awayGoals : a.homeGoals));
        const diffB = Math.abs((b.isHome ? b.homeGoals : b.awayGoals) - (b.isHome ? b.awayGoals : b.homeGoals));
        return diffB - diffA;
      })
      .slice(0, 5)
  );

  const worstLosses = $derived(
    [...filteredMatches]
      .filter(m => m.result === 'L')
      .sort((a, b) => {
        const diffA = Math.abs((a.isHome ? a.homeGoals : a.awayGoals) - (a.isHome ? a.awayGoals : a.homeGoals));
        const diffB = Math.abs((b.isHome ? b.homeGoals : b.awayGoals) - (b.isHome ? b.awayGoals : b.homeGoals));
        return diffB - diffA;
      })
      .slice(0, 5)
  );
</script>

<div class="min-h-screen">
  
  <!-- Header -->
  <header class="sticky top-0 z-50 border-b border-white/10 bg-black/50 backdrop-blur-xl">
    <div class="container mx-auto px-4 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full bg-independiente-red flex items-center justify-center shadow-lg shadow-independiente-red/30">
          <Flame class="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 class="text-xl font-black text-white tracking-tight">HISTORIA ROJA</h1>
          <p class="text-xs text-white/50">Club Atlético Independiente</p>
        </div>
      </div>

      <nav class="hidden md:flex items-center gap-1">
        <TabsTrigger 
          value="matches" 
          onclick={(v) => activeTab = v}
          isActive={activeTab === 'matches'}
        >
          Partidos
        </TabsTrigger>
        <TabsTrigger 
          value="stats" 
          onclick={(v) => activeTab = v}
          isActive={activeTab === 'stats'}
        >
          Estadísticas
        </TabsTrigger>
        <TabsTrigger 
          value="teams" 
          onclick={(v) => activeTab = v}
          isActive={activeTab === 'teams'}
        >
          Equipos
        </TabsTrigger>
      </nav>

      <Button 
        variant="ghost" 
        size="icon"
        class="md:hidden"
        onclick={() => isMenuOpen = !isMenuOpen}
      >
        <Filter class="w-5 h-5" />
      </Button>
    </div>

    {#if isMenuOpen}
      <div class="md:hidden border-t border-white/10 bg-black/80 backdrop-blur-xl p-4">
        <div class="flex flex-col gap-2">
          <Button 
            variant={activeTab === 'matches' ? 'default' : 'ghost'}
            class="w-full justify-start"
            onclick={() => { activeTab = 'matches'; isMenuOpen = false; }}
          >
            Partidos
          </Button>
          <Button 
            variant={activeTab === 'stats' ? 'default' : 'ghost'}
            class="w-full justify-start"
            onclick={() => { activeTab = 'stats'; isMenuOpen = false; }}
          >
            Estadísticas
          </Button>
          <Button 
            variant={activeTab === 'teams' ? 'default' : 'ghost'}
            class="w-full justify-start"
            onclick={() => { activeTab = 'teams'; isMenuOpen = false; }}
          >
            Equipos
          </Button>
        </div>
      </div>
    {/if}
  </header>

  <!-- Main Content -->
  <main class="container mx-auto px-4 py-8">
    
    {#if activeTab === 'matches'}
      
      <!-- Hero Stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
          <div class="flex items-center gap-2 mb-2">
            <History class="w-4 h-4 text-independiente-red" />
            <span class="text-xs text-white/60 uppercase font-medium">Total</span>
          </div>
          <p class="text-3xl font-black text-white">{stats.totalMatches}</p>
          <p class="text-xs text-white/40">partidos jugados</p>
        </div>

        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
          <div class="flex items-center gap-2 mb-2">
            <Trophy class="w-4 h-4 text-green-400" />
            <span class="text-xs text-white/60 uppercase font-medium">Victorias</span>
          </div>
          <p class="text-3xl font-black text-green-400">{stats.wins}</p>
          <p class="text-xs text-white/40">{((stats.wins / stats.totalMatches) * 100).toFixed(1)}%</p>
        </div>

        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
          <div class="flex items-center gap-2 mb-2">
            <Swords class="w-4 h-4 text-yellow-400" />
            <span class="text-xs text-white/60 uppercase font-medium">Empates</span>
          </div>
          <p class="text-3xl font-black text-yellow-400">{stats.draws}</p>
          <p class="text-xs text-white/40">{((stats.draws / stats.totalMatches) * 100).toFixed(1)}%</p>
        </div>

        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
          <div class="flex items-center gap-2 mb-2">
            <Shield class="w-4 h-4 text-red-400" />
            <span class="text-xs text-white/60 uppercase font-medium">Derrotas</span>
          </div>
          <p class="text-3xl font-black text-red-400">{stats.losses}</p>
          <p class="text-xs text-white/40">{((stats.losses / stats.totalMatches) * 100).toFixed(1)}%</p>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10 mb-6">
        <div class="flex flex-col md:flex-row gap-4">
          <div class="flex-1 relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40" />
            <Input 
              bind:value={searchQuery}
              placeholder="Buscar equipo..."
              class="pl-10"
            />
          </div>
          
          <div class="flex gap-2">
            <Select bind:value={resultFilter} placeholder="Resultado" class="w-40">
              <option value="">Todos</option>
              <option value="W">Victoria</option>
              <option value="L">Derrota</option>
              <option value="D">Empate</option>
            </Select>
            
            <Select bind:value={locationFilter} placeholder="Ubicación" class="w-40">
              <option value="">Todos</option>
              <option value="home">Local</option>
              <option value="away">Visitante</option>
            </Select>
          </div>
        </div>
      </div>

      <!-- Match List -->
      <div class="space-y-3">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-white">Partidos ({filteredMatches.length})</h2>
          
          <div class="flex gap-2">
            <Badge variant="success">{filteredMatches.filter(m => m.result === 'W').length} V</Badge>
            <Badge variant="secondary">{filteredMatches.filter(m => m.result === 'D').length} E</Badge>
            <Badge variant="destructive">{filteredMatches.filter(m => m.result === 'L').length} D</Badge>
          </div>
        </div>

        {#if filteredMatches.length === 0}
          <div class="text-center py-12">
            <Shield class="w-12 h-12 text-white/20 mx-auto mb-4" />
            <p class="text-white/50">No se encontraron partidos</p>
          </div>
        {:else}
          <div class="space-y-3">
            {#each filteredMatches as match (match.id)}
              <MatchCard {match} />
            {/each}
          </div>
        {/if}
      </div>
    
    {:else if activeTab === 'stats'}
      
      <!-- Statistics Dashboard -->
      <div class="space-y-8">
        
        <!-- Main Stats -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatsCard 
            title="Partidos Jugados"
            value={stats.totalMatches}
            subtitle="Total de encuentros"
            iconContent="📊"
          />

          <StatsCard 
            title="Goles a Favor"
            value={stats.goalsScored}
            subtitle="Promedio: {(stats.goalsScored / stats.totalMatches).toFixed(2)} por partido"
            iconContent="⚽"
          />

          <StatsCard 
            title="Goles en Contra"
            value={stats.goalsConceded}
            subtitle="Promedio: {(stats.goalsConceded / stats.totalMatches).toFixed(2)} por partido"
            iconContent="🛡️"
          />

          <StatsCard 
            title="Diferencia de Gol"
            value={stats.goalDifference > 0 ? '+' + stats.goalDifference : stats.goalDifference}
            subtitle="Balance total"
            iconContent="📈"
          />
        </div>

        <!-- Biggest Wins -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <div class="flex items-center gap-3 mb-6">
              <div class="p-2 rounded-lg bg-green-500/20">
                <Trophy class="w-5 h-5 text-green-400" />
              </div>
              <h3 class="text-lg font-bold text-white">Mayores Victorias</h3>
            </div>
            
            <div class="space-y-3">
              {#each biggestWins as match}
                <MatchCard {match} />
              {/each}
            </div>
          </div>

          <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <div class="flex items-center gap-3 mb-6">
              <div class="p-2 rounded-lg bg-red-500/20">
                <Shield class="w-5 h-5 text-red-400" />
              </div>
              <h3 class="text-lg font-bold text-white">Peores Derrotas</h3>
            </div>
            
            <div class="space-y-3">
              {#each worstLosses as match}
                <MatchCard {match} />
              {/each}
            </div>
          </div>
        </div>
      </div>
    
    {:else if activeTab === 'teams'}
      
      <div class="space-y-6">
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <div class="flex items-center gap-3 mb-6">
            <div class="p-2 rounded-lg bg-independiente-red/20">
              <Swords class="w-5 h-5 text-independiente-red" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-white">Rendimiento por Equipo</h3>
              <p class="text-sm text-white/50">Tabla de posiciones contra cada rival</p>
            </div>
          </div>
          
          <TeamStatsTable stats={teamStats} />
        </div>
      </div>
    {/if}
  </main>

  <!-- Footer -->
  <footer class="border-t border-white/10 bg-black/30 backdrop-blur-sm mt-12">
    <div class="container mx-auto px-4 py-6">
      <div class="flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2">
          <Flame class="w-5 h-5 text-independiente-red" />
          <span class="text-sm text-white/60">Historia Roja © 2025</span>
        </div>
        
        <p class="text-sm text-white/40">
          Club Atlético Independiente - El Orgullo Nacional
        </p>
      </div>
    </div>
  </footer>
</div>