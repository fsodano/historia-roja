<script lang="ts">
  import { cn } from "../../utils";
  import type { Snippet } from "svelte";

  let {
    children,
    class: className = "",
    value = "",
    onclick,
    isActive = false
  }: {
    children: Snippet;
    class?: string;
    value?: string;
    onclick?: (value: string) => void;
    isActive?: boolean;
  } = $props();
</script>

<button
  onclick={() => onclick?.(value)}
  class={cn(
    "inline-flex items-center justify-center whitespace-nowrap rounded-md px-4 py-2 text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-independiente-red",
    isActive
      ? "bg-independiente-red text-white"
      : "hover:bg-white/10 text-white/70 hover:text-white",
    className
  )}
>
  {@render children()}
</button>