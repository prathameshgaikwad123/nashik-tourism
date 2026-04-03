
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { Button } from "@/components/ui/button";
import { MapPin, Clock, Calendar } from "lucide-react";

const Pandavleni = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <div className="h-[50vh] relative">
          <img 
            src="https://images.unsplash.com/photo-1590274853856-f22d5ee1c03f?q=80&w=2071&auto=format&fit=crop"
            alt="Pandavleni Caves"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black/40" />
          <div className="absolute inset-0 flex items-center">
            <div className="container">
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">Pandavleni Caves</h1>
              <p className="text-lg text-white/90 max-w-2xl">
                Ancient Buddhist caves showcasing remarkable architecture and history
              </p>
            </div>
          </div>
        </div>

        <div className="container py-12">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="md:col-span-2">
              <h2 className="text-2xl font-bold mb-4">About Pandavleni Caves</h2>
              <p className="text-muted-foreground mb-6">
                The Pandavleni Caves, also known as Trirashmi Caves, are a group of 24 caves carved 
                between the 3rd century BCE and 2nd century CE. These caves represent one of the most 
                important examples of ancient Indian rock-cut architecture and Buddhist heritage.
              </p>
              
              <h3 className="text-xl font-semibold mb-3">Cave Features</h3>
              <ul className="space-y-2 mb-6 list-disc list-inside text-muted-foreground">
                <li>24 rock-cut caves</li>
                <li>Ancient inscriptions</li>
                <li>Buddhist sculptures</li>
                <li>Meditation chambers</li>
                <li>Water cisterns</li>
              </ul>

              <Button size="lg">Plan Your Visit</Button>
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
                        Pandavleni Caves, Mumbai-Agra Highway, Nashik, Maharashtra 422003
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <Clock className="w-5 h-5 mt-1 text-primary" />
                    <div>
                      <h4 className="font-medium">Opening Hours</h4>
                      <p className="text-sm text-muted-foreground">
                        8:30 AM - 5:30 PM<br />
                        Open all days
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <Calendar className="w-5 h-5 mt-1 text-primary" />
                    <div>
                      <h4 className="font-medium">Best Time to Visit</h4>
                      <p className="text-sm text-muted-foreground">
                        October to March<br />
                        Early morning for better photography
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

export default Pandavleni;
