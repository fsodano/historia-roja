<script lang="ts">
  import { cn } from "../../utils";
  import type { Snippet } from "svelte";

  let { 
    children,
    class: className = "",
    variant = "default",
    size = "default",
    onclick,
    disabled = false,
    type = "button"
  }: {
    children: Snippet;
    class?: string;
    variant?: "default" | "destructive" | "outline" | "secondary" | "ghost" | "link";
    size?: "default" | "sm" | "lg" | "icon";
    onclick?: (e: MouseEvent) => void;
    disabled?: boolean;
    type?: "button" | "submit" | "reset";
  } = $props();

  const variantStyles = {
    default: "bg-independiente-red text-white hover:bg-independiente-dark",
    destructive: "bg-red-600 text-white hover:bg-red-700",
    outline: "border border-independiente-red bg-transparent hover:bg-independiente-red/10 text-white",
    secondary: "bg-independiente-gold text-independiente-black hover:bg-yellow-400",
    ghost: "hover:bg-white/10 text-white",
    link: "text-independiente-red underline-offset-4 hover:underline"
  };

  const sizeStyles = {
    default: "h-10 px-4 py-2",
    sm: "h-8 px-3 text-sm",
    lg: "h-12 px-8 text-lg",
    icon: "h-10 w-10"
  };
</script>

<button
  {type}
  {disabled}
  onclick={onclick}
  class={cn(
    "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-independiente-red disabled:pointer-events-none disabled:opacity-50",
    variantStyles[variant],
    sizeStyles[size],
    className
  )}
>
  {@render children()}
</button>