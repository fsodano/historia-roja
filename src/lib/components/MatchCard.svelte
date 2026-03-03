<script lang="ts">
  import { cn } from "../utils";
  import Badge from "./ui/badge.svelte";
  import type { Match } from "../types";

  let { match, class: className = "" }: { match: Match; class?: string } = $props();

  const getResultVariant = (result: string) => {
    switch (result) {
      case 'W': return 'success';
      case 'L': return 'destructive';
      case 'D': return 'secondary';
      default: return 'default';
    }
  };

  const getResultLabel = (result: string) => {
    switch (result) {
      case 'W': return 'Victoria';
      case 'L': return 'Derrota';
      case 'D': return 'Empate';
      default: return result;
    }
  };
</script>

<div
  class={cn(
    "group relative overflow-hidden rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm p-4 transition-all duration-300 hover:bg-white/10 hover:border-independiente-red/30 hover:shadow-lg hover:shadow-independiente-red/10",
    className
  )}
>
  <div class="absolute inset-0 bg-gradient-to-r from-independiente-red/0 via-independiente-red/5 to-independiente-red/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
  
  <div class="relative flex items-center justify-between gap-4">
    <div class="flex-1 flex items-center gap-3">
      <div class={cn(
        "w-2 h-12 rounded-full transition-colors duration-300",
        match.result === 'W' ? "bg-green-500" : match.result === 'L' ? "bg-red-500" : "bg-yellow-500"
      )}></div>
      
      <div class="flex-1">
        <div class="flex items-center gap-2 text-sm text-white/60 mb-1">
          <span class={cn("font-medium", match.isHome ? "text-independiente-red" : "text-white/80")}>
            {match.isHome ? "Local" : "Visitante"}
          </span>
          <span class="text-white/30">•</span>
          <span>{match.opponent}</span>
        </div>
        
        <div class="flex items-center gap-3">
          <span class="text-lg font-bold text-white">{match.homeTeam}</span>
          <div class="flex items-center gap-1 px-3 py-1 rounded-lg bg-white/10">
            <span class="text-xl font-black text-independiente-red">{match.homeGoals}</span>
            <span class="text-white/40">-</span>
            <span class="text-xl font-black text-independiente-red">{match.awayGoals}</span>
          </div>
          <span class="text-lg font-bold text-white">{match.awayTeam}</span>
        </div>
      </div>
    </div>

    <Badge variant={getResultVariant(match.result)} class="shrink-0">
      {getResultLabel(match.result)}
    </Badge>
  </div>
</div>