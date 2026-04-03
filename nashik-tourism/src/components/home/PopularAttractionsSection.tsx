
import { Link } from "react-router-dom";
import { ArrowRight, Star } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const attractions = [
  {
    name: "Sula Vineyards",
    image: "https://images.unsplash.com/photo-1560830889-5c5c15827b84?q=80&w=2070&auto=format&fit=crop",
    description: "India's premier winery offering tours, tastings, and fine dining.",
    rating: 4.8,
    link: "/discover/sula-vineyards"
  },
  {
    name: "Trimbakeshwar Temple",
    image: "https://images.unsplash.com/photo-1642740041801-cbe307fc400c?q=80&w=2035&auto=format&fit=crop",
    description: "Ancient Shiva temple, one of the 12 Jyotirlinga shrines in India.",
    rating: 4.7,
    link: "/discover/trimbakeshwar"
  },
  {
    name: "Pandavleni Caves",
    image: "https://images.unsplash.com/photo-1590274853856-f22d5ee1c03f?q=80&w=2071&auto=format&fit=crop",
    description: "24 ancient Buddhist caves dating back to the 1st century BC.",
    rating: 4.5,
    link: "/discover/pandavleni"
  }
];

export function PopularAttractionsSection() {
  return (
    <section className="py-16 bg-accent/20">
      <div className="container">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold">Popular Attractions</h2>
          <Button asChild variant="outline">
            <Link to="/discover">
              View All
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {attractions.map(attraction => (
            <Card key={attraction.name} className="overflow-hidden card-hover">
              <div className="relative h-60">
                <img src={attraction.image} alt={attraction.name} className="w-full h-full object-cover" />
              </div>
              <CardContent className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold">{attraction.name}</h3>
                  <div className="flex items-center text-orange-500">
                    <Star className="h-4 w-4 fill-current" />
                    <span className="ml-1 text-sm">{attraction.rating}</span>
                  </div>
                </div>
                <p className="text-muted-foreground mb-4">{attraction.description}</p>
                <Button asChild variant="outline" size="sm">
                  <Link to={attraction.link}>Learn More</Link>
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
