
import { Link } from "react-router-dom";
import { ArrowRight, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";

export function HeroSection() {
  return (
    <section className="relative h-[80vh] overflow-hidden">
      <div className="absolute inset-0 bg-cover bg-center" style={{
        backgroundImage: "url('https://images.unsplash.com/photo-1600967499257-02245b2439d2?q=80&w=2069&auto=format&fit=crop')"
      }} />
      <div className="absolute inset-0 hero-gradient" />
      <div className="container relative z-10 h-full flex flex-col justify-center items-start text-white"
        style={{
          backgroundImage: "url('https://images.unsplash.com/photo-1482938289607-e9573fc25ebb?auto=format&fit=crop&q=80&w=3648&h=5472')",
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat"
        }}
      >
        <h1 className="text-4xl md:text-6xl font-bold mb-4 animate-fade-in">
          Discover the Spiritual <br className="hidden md:block" />
          Heart of India
        </h1>
        <p className="text-xl mb-8 max-w-2xl animate-fade-in">
          Explore Nashik's rich cultural heritage, sacred temples, and the upcoming Kumbh Mela 2027.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 animate-fade-in">
          <Button asChild size="lg" className="text-md">
            <Link to="/plan-trip">
              Plan Your Trip
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg" className="bg-white/10 backdrop-blur-sm text-md hover:bg-white/20">
            <Link to="/kumbh-mela">
              Kumbh Mela 2027
              <Calendar className="ml-2 h-5 w-5" />
            </Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
