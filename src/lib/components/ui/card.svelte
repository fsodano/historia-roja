<script lang="ts">
  import { cn } from "../../utils";
  import type { Snippet } from "svelte";

  let { 
    children,
    class: className = ""
  }: {
    children: Snippet;
    class?: string;
  } = $props();
</script>

<div
  class={cn(
    "rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm text-white shadow-xl",
    className
  )}
>
  {@render children()}
</div>