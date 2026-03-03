<script lang="ts">
  import { cn } from "../utils";
  import Card from "./ui/card.svelte";

  let { 
    title, 
    value, 
    subtitle,
    trend,
    iconContent,
    class: className = ""
  }: { 
    title: string; 
    value: string | number; 
    subtitle?: string;
    trend?: { value: number; positive: boolean };
    iconContent?: string;
    class?: string;
  } = $props();
</script>

<Card class={cn("p-6 relative overflow-hidden group", className)}>
  <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-independiente-red/20 to-transparent rounded-bl-full opacity-50 group-hover:opacity-70 transition-opacity"></div>
  
  <div class="relative">
    <div class="flex items-start justify-between">
      <div>
        <p class="text-sm font-medium text-white/60 mb-1">{title}</p>
        <div class="flex items-baseline gap-2">
          <h3 class="text-3xl font-black text-white tracking-tight">{value}</h3>
          
          {#if trend}
            <span class={cn(
              "text-sm font-medium flex items-center gap-0.5",
              trend.positive ? "text-green-400" : "text-red-400"
            )}>
              {trend.positive ? '+' : ''}{trend.value}%
            </span>
          {/if}
        </div>
        
        {#if subtitle}
          <p class="text-xs text-white/40 mt-1">{subtitle}</p>
        {/if}
      </div>
      
      <div class="p-2 rounded-lg bg-white/5 text-independiente-red">
        {#if iconContent}
          <span class="text-2xl">{iconContent}</span>
        {/if}
      </div>
    </div>
  </div>
</Card>