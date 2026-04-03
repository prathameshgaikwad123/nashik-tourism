
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { Button } from "@/components/ui/button";
import { MapPin, Clock, Calendar } from "lucide-react";

const Trimbakeshwar = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <div className="h-[50vh] relative">
          <img 
            src="https://images.unsplash.com/photo-1642740041801-cbe307fc400c?q=80&w=2035&auto=format&fit=crop"
            alt="Trimbakeshwar Temple"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-black/40" />
          <div className="absolute inset-0 flex items-center">
            <div className="container">
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">Trimbakeshwar Temple</h1>
              <p className="text-lg text-white/90 max-w-2xl">
                One of the twelve Jyotirlinga shrines of Lord Shiva
              </p>
            </div>
          </div>
        </div>

        <div className="container py-12">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="md:col-span-2">
              <h2 className="text-2xl font-bold mb-4">About Trimbakeshwar Temple</h2>
              <p className="text-muted-foreground mb-6">
                The Trimbakeshwar Temple is an ancient Hindu temple dedicated to Lord Shiva and is one of 
                the twelve Jyotirlinga shrines. The temple's architecture reflects the Nagara style, and it 
                is situated at the source of the Godavari River, making it one of the most sacred sites in India.
              </p>
              
              <h3 className="text-xl font-semibold mb-3">Temple Highlights</h3>
              <ul className="space-y-2 mb-6 list-disc list-inside text-muted-foreground">
                <li>Three-tiered temple structure</li>
                <li>Black stone construction</li>
                <li>Source of Godavari River</li>
                <li>Ancient inscriptions</li>
                <li>Sacred Kushavarta Tirth</li>
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
                        Trimbak, Nashik District, Maharashtra 422212
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-3">
                    <Clock className="w-5 h-5 mt-1 text-primary" />
                    <div>
                      <h4 className="font-medium">Darshan Hours</h4>
                      <p className="text-sm text-muted-foreground">
                        5:30 AM - 9:00 PM<br />
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
                        Early morning for peaceful darshan
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

export default Trimbakeshwar;
