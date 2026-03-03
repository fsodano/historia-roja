<script lang="ts">
  import { cn } from "../utils";
  import type { TeamStats } from "../types";

  let { stats, class: className = "" }: { stats: TeamStats[]; class?: string } = $props();

  const sortedStats = $derived([...stats].sort((a, b) => {
    const pointsA = a.wins * 3 + a.draws;
    const pointsB = b.wins * 3 + b.draws;
    return pointsB - pointsA;
  }));
</script>

<div class={cn("overflow-hidden rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm", className)}>
  <div class="overflow-x-auto">
    <table class="w-full">
      <thead>
        <tr class="border-b border-white/10 bg-white/5">
          <th class="px-4 py-3 text-left text-xs font-medium text-white/60 uppercase tracking-wider">Equipo</th>
          <th class="px-4 py-3 text-center text-xs font-medium text-white/60 uppercase tracking-wider">PJ</th>
          <th class="px-4 py-3 text-center text-xs font-medium text-white/60 uppercase tracking-wider">PG</th>
          <th class="px-4 py-3 text-center text-xs font-medium text-white/60 uppercase tracking-wider">PE</th>
          <th class="px-4 py-3 text-center text-xs font-medium text-white/60 uppercase tracking-wider">PP</th>
          <th class="px-4 py-3 text-center text-xs font-medium text-white/60 uppercase tracking-wider">GF</th>
          <th class="px-4 py-3 text-center text-xs font-medium text-white/60 uppercase tracking-wider">GC</th>
          <th class="px-4 py-3 text-center text-xs font-medium text-white/60 uppercase tracking-wider">DG</th>
          <th class="px-4 py-3 text-center text-xs font-medium text-white/60 uppercase tracking-wider">Pts</th>
        </tr>
      </thead>
      
      <tbody class="divide-y divide-white/5">
        {#each sortedStats as team, index}
          <tr class="hover:bg-white/5 transition-colors">
            <td class="px-4 py-3">
              <div class="flex items-center gap-3">
                <span class={cn(
                  "w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold",
                  index < 3 ? "bg-independiente-red text-white" : "bg-white/10 text-white/60"
                )}>
                  {index + 1}
                </span>
                <span class="text-sm font-medium text-white">{team.team}</span>
              </div>
            </td>
            <td class="px-4 py-3 text-center text-sm text-white/80">{team.played}</td>
            <td class="px-4 py-3 text-center text-sm text-green-400 font-medium">{team.wins}</td>
            <td class="px-4 py-3 text-center text-sm text-yellow-400 font-medium">{team.draws}</td>
            <td class="px-4 py-3 text-center text-sm text-red-400 font-medium">{team.losses}</td>
            <td class="px-4 py-3 text-center text-sm text-white/80">{team.goalsFor}</td>
            <td class="px-4 py-3 text-center text-sm text-white/80">{team.goalsAgainst}</td>
            <td class="px-4 py-3 text-center text-sm font-medium {team.goalsFor - team.goalsAgainst >= 0 ? 'text-green-400' : 'text-red-400'}">
              {team.goalsFor - team.goalsAgainst > 0 ? '+' : ''}{team.goalsFor - team.goalsAgainst}
            </td>
            <td class="px-4 py-3 text-center">
              <span class="text-sm font-black text-independiente-red">{team.wins * 3 + team.draws}</span>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>