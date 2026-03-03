<script lang="ts">
  import { cn } from "../../utils";

  let { 
    class: className = "",
    value = $bindable(""),
    placeholder = "",
    type = "text"
  }: {
    class?: string;
    value?: string;
    placeholder?: string;
    type?: string;
  } = $props();
</script>

<input
  {type}
  bind:value
  {placeholder}
  class={cn(
    "flex h-10 w-full rounded-md border border-white/20 bg-white/5 px-3 py-2 text-sm text-white placeholder:text-white/50 focus:outline-none focus:ring-2 focus:ring-independiente-red focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50",
    className
  )}
/>