<script lang="ts">
  import { cn } from "../../utils";
  import type { Snippet } from "svelte";

  let { 
    children,
    class: className = "",
    value = $bindable(""),
    placeholder = "Select..."
  }: {
    children: Snippet;
    class?: string;
    value?: string;
    placeholder?: string;
  } = $props();
</script>

<select
  bind:value
  class={cn(
    "flex h-10 w-full rounded-md border border-white/20 bg-white/5 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-independiente-red focus:border-transparent disabled:cursor-not-allowed disabled:opacity-50 appearance-none cursor-pointer",
    className
  )}
>
  <option value="" disabled class="bg-independiente-black">{placeholder}</option>
  {@render children()}
</select>