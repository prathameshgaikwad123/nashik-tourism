
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { Button } from "@/components/ui/button";
import { MapPin, Clock, Calendar } from "lucide-react";

const SulaVineyards = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <div className="h-[50vh] relative">
          <img 
            src="https://images.unsplash.com/photo-1560830889-5c5c15827b84?q=80&w=2070&auto=format&fit=crop"
            alt="Sula Vineyards"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black/40" />
          <div className="absolute inset-0 flex items-center">
            <div className="container">
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">Sula Vineyards</h1>
              <p className="text-lg text-white/90 max-w-2xl">
                India's premier winery offering tours, tastings, and fine dining experiences
              </p>
            </div>
          </div>
        </div>

        <div className="container py-12">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="md:col-span-2">
              <h2 className="text-2xl font-bold mb-4">About Sula Vineyards</h2>
              <p className="text-muted-foreground mb-6">
                Established in 1999, Sula Vineyards pioneered the wine-making industry in India's Nashik Valley. 
                Today, it's India's most visited vineyard, offering world-class wines, guided tours, tastings, 
                and luxury accommodations with stunning views of the surrounding hills.
              </p>
              
              <h3 className="text-xl font-semibold mb-3">Activities & Experiences</h3>
              <ul className="space-y-2 mb-6 list-disc list-inside text-muted-foreground">
                <li>Guided winery tours</li>
                <li>Wine tasting sessions</li>
                <li>Grape stomping (seasonal)</li>
                <li>Fine dining restaurants</li>
                <li>Weekend music events</li>
              </ul>

              <Button size="lg">Book a Tour</Button>
            </div>

            <div className="space-y-6">
              <div className="bg-card rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-4">Visitor Information</h3>
                
                <div className="space-y-4">
                  <div className="flex items-start gap-3">
                    <MapPin className="w-5 h-5 mt-1 text-primary" />
                    <div>
                      <h4 className="font-medium">Location</h4>
                      <p className="text-sm text-muted-foreground">
                        Gat 36/2, Govardhan Village, Nashik, Maharashtra 422222
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <Clock className="w-5 h-5 mt-1 text-primary" />
                    <div>
                      <h4 className="font-medium">Opening Hours</h4>
                      <p className="text-sm text-muted-foreground">
                        11:00 AM - 10:00 PM<br />
                        Open all days
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <Calendar className="w-5 h-5 mt-1 text-primary" />
                    <div>
                      <h4 className="font-medium">Best Time to Visit</h4>
                      <p className="text-sm text-muted-foreground">
                        November to March<br />
                        Grape harvesting season: January-March
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default SulaVineyards;
