
import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

export function KumbhMelaSection() {
  return (
    <section className="py-16 container">
      <div className="flex flex-col md:flex-row gap-8 items-center">
        <div className="md:w-1/2">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Kumbh Mela 2027
          </h2>
          <p className="text-lg mb-6">
            Experience one of the world's largest spiritual gatherings right here in Nashik. Plan your visit to this sacred event that happens once every 12 years.
          </p>
          <ul className="space-y-3 mb-6">
            <li className="flex items-start gap-2">
              <div className="h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                <span className="text-primary text-sm">✓</span>
              </div>
              <span>Comprehensive event calendar and key dates</span>
            </li>
            <li className="flex items-start gap-2">
              <div className="h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                <span className="text-primary text-sm">✓</span>
              </div>
              <span>Accommodation options for all budgets</span>
            </li>
            <li className="flex items-start gap-2">
              <div className="h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                <span className="text-primary text-sm">✓</span>
              </div>
              <span>Safety tips and travel guidelines</span>
            </li>
          </ul>
          <Button asChild>
            <Link to="/kumbh-mela">
              Learn More About Kumbh Mela
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
        <div className="md:w-1/2">
          <div className="rounded-lg overflow-hidden shadow-lg">
            <img src="https://images.unsplash.com/photo-1592462029627-efb7d3bc2fe1?q=80&w=2070&auto=format&fit=crop" alt="Kumbh Mela celebration" className="w-full h-[400px] object-cover" />
          </div>
        </div>
      </div>
    </section>
  );
}
