<script lang="ts">
  import { cn } from "../../utils";
  import type { Snippet } from "svelte";

  let { 
    children,
    class: className = "",
    variant = "default"
  }: {
    children: Snippet;
    class?: string;
    variant?: "default" | "secondary" | "destructive" | "outline" | "success" | "warning";
  } = $props();

  const variantStyles = {
    default: "bg-independiente-red text-white hover:bg-independiente-dark",
    secondary: "bg-independiente-gold text-independiente-black hover:bg-yellow-400",
    destructive: "bg-red-600 text-white",
    outline: "border border-white/20 bg-transparent text-white",
    success: "bg-green-600 text-white",
    warning: "bg-yellow-600 text-white"
  };
</script>

<span
  class={cn(
    "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-independiente-red focus:ring-offset-2",
    variantStyles[variant],
    className
  )}
>
  {@render children()}
</span>