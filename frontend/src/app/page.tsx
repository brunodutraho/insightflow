import Navbar from "@/components/Landing/Navbar";
import Hero from "@/components/Landing/Hero";
import Features from "@/components/Landing/Features";
import CTA from "@/components/Landing/CTA";

export default function Home() {
  return (
    <main className="bg-brand-dark text-brand-text min-h-screen">
      <Navbar />
      <Hero />
      <Features />
      <CTA />
    </main>
  );
}