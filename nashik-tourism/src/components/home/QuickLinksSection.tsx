
import { Link } from "react-router-dom";
import { Compass, MapPin, Hotel, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export function QuickLinksSection() {
  return (
    <section className="py-16 bg-accent/30">
      <div className="container">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <Card className="card-hover">
            <CardContent className="p-6 flex flex-col items-center text-center">
              <div className="h-14 w-14 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                <Compass className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Explore Attractions</h3>
              <p className="text-muted-foreground mb-4">
                Discover ancient temples, scenic vineyards, and historic caves.
              </p>
              <Button asChild variant="outline">
                <Link to="/discover">
                  View Destinations
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </CardContent>
          </Card>
          
          <Card className="card-hover">
            <CardContent className="p-6 flex flex-col items-center text-center">
              <div className="h-14 w-14 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                <MapPin className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Plan My Trip</h3>
              <p className="text-muted-foreground mb-4">
                Create personalized itineraries for your perfect Nashik experience.
              </p>
              <Button asChild variant="outline">
                <Link to="/plan-trip">
                  Build Itinerary
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </CardContent>
          </Card>
          
          <Card className="card-hover">
            <CardContent className="p-6 flex flex-col items-center text-center">
              <div className="h-14 w-14 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                <Hotel className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Book Hotels</h3>
              <p className="text-muted-foreground mb-4">
                Find accommodation options from luxury resorts to budget stays.
              </p>
              <Button asChild variant="outline">
                <Link to="/hotels">
                  Find Accommodation
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
