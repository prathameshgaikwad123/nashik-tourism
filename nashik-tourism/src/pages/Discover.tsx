
import { useState } from "react";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link } from "react-router-dom";
import { ArrowRight, Search, MapPin, Clock, Star } from "lucide-react";

const attractions = [
  {
    id: "sula-vineyards",
    name: "Sula Vineyards",
    image: "https://images.unsplash.com/photo-1560830889-5c5c15827b84?q=80&w=2070&auto=format&fit=crop",
    description: "India's premier winery offering tours, tastings, and fine dining with beautiful vineyard views.",
    rating: 4.8,
    location: "Nashik",
    duration: "3-4 hours",
    category: "Wineries"
  },
  {
    id: "trimbakeshwar",
    name: "Trimbakeshwar Temple",
    image: "https://images.unsplash.com/photo-1642740041801-cbe307fc400c?q=80&w=2035&auto=format&fit=crop",
    description: "One of the twelve Jyotirlinga shrines of Lord Shiva, featuring ancient architecture and spiritual significance.",
    rating: 4.7,
    location: "Trimbak",
    duration: "2-3 hours",
    category: "Temples"
  },
  {
    id: "pandavleni",
    name: "Pandavleni Caves",
    image: "https://images.unsplash.com/photo-1590274853856-f22d5ee1c03f?q=80&w=2071&auto=format&fit=crop",
    description: "Ancient Buddhist caves dating back to the 1st century BC, featuring intricate carvings and historical architecture.",
    rating: 4.5,
    location: "Nashik",
    duration: "2 hours",
    category: "Historical"
  },
  {
    id: "coin-museum",
    name: "Indian Institute of Research in Numismatic Studies",
    image: "https://images.unsplash.com/photo-1621675523821-6a0d5cc8d6f1?q=80&w=2070&auto=format&fit=crop",
    description: "Asia's only museum dedicated to the study of coins, showcasing a vast collection from different periods of Indian history.",
    rating: 4.3,
    location: "Anjaneri",
    duration: "1-2 hours",
    category: "Museums"
  },
  {
    id: "someshwar",
    name: "Someshwar Waterfall",
    image: "https://images.unsplash.com/photo-1523867574998-1a336b6ded04?q=80&w=1974&auto=format&fit=crop",
    description: "A scenic waterfall surrounded by lush greenery, perfect for nature lovers and photography enthusiasts.",
    rating: 4.4,
    location: "Nashik",
    duration: "2-3 hours",
    category: "Nature"
  },
  {
    id: "saptashrungi",
    name: "Saptashrungi Devi Temple",
    image: "https://images.unsplash.com/photo-1623841675698-8a9b63d8746a?q=80&w=1974&auto=format&fit=crop",
    description: "One of the 51 Shakti Peethas, situated on a hill offering panoramic views of the surrounding landscape.",
    rating: 4.6,
    location: "Vani",
    duration: "3-4 hours",
    category: "Temples"
  },
  {
    id: "muktidham",
    name: "Muktidham Temple",
    image: "https://images.unsplash.com/photo-1627894006066-b45674e5e25e?q=80&w=2070&auto=format&fit=crop",
    description: "A beautiful white marble temple complex with replicas of the twelve Jyotirlingas of Lord Shiva.",
    rating: 4.5,
    location: "Nashik",
    duration: "1-2 hours",
    category: "Temples"
  },
  {
    id: "york-winery",
    name: "York Winery",
    image: "https://images.unsplash.com/photo-1612203985729-70726954388c?q=80&w=1974&auto=format&fit=crop",
    description: "A boutique winery offering premium wine tastings, vineyard tours, and spectacular views of the Gangapur Dam.",
    rating: 4.6,
    location: "Gangapur",
    duration: "2-3 hours",
    category: "Wineries"
  },
  {
    id: "kalaram-temple",
    name: "Kalaram Temple",
    image: "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?q=80&w=2069&auto=format&fit=crop",
    description: "An ancient temple known for its black stone idol of Lord Rama and historical significance in social reform movements.",
    rating: 4.4,
    location: "Panchavati",
    duration: "1-2 hours",
    category: "Temples"
  },
];

const categories = [
  "All",
  "Temples",
  "Wineries",
  "Historical",
  "Nature",
  "Museums"
];

const Discover = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  
  const filteredAttractions = attractions.filter(attraction => {
    const matchesSearch = attraction.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                         attraction.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === "All" || attraction.category === selectedCategory;
    
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative h-[40vh] overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: "url('https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?q=80&w=2069&auto=format&fit=crop')",
          }}
        />
        <div className="absolute inset-0 hero-gradient" />
        <div className="container relative z-10 h-full flex flex-col justify-center items-center text-white text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">
            Discover Nashik
          </h1>
          <p className="text-xl mb-6 max-w-2xl">
            Explore ancient temples, scenic vineyards, and cultural treasures in the divine city of Nashik.
          </p>
        </div>
      </section>
      
      {/* Search and Filter Section */}
      <section className="py-8 bg-accent/30">
        <div className="container">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-grow">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search attractions, activities, etc."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0">
              {categories.map((category) => (
                <Button
                  key={category}
                  variant={selectedCategory === category ? "default" : "outline"}
                  onClick={() => setSelectedCategory(category)}
                  className="whitespace-nowrap"
                >
                  {category}
                </Button>
              ))}
            </div>
          </div>
        </div>
      </section>
      
      {/* Attractions Grid */}
      <section className="py-12 container">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAttractions.map((attraction) => (
            <Card key={attraction.id} className="overflow-hidden card-hover">
              <div className="relative h-60">
                <img 
                  src={attraction.image} 
                  alt={attraction.name} 
                  className="w-full h-full object-cover"
                />
              </div>
              <CardContent className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold">{attraction.name}</h3>
                  <div className="flex items-center text-nashik-orange">
                    <Star className="h-4 w-4 fill-current" />
                    <span className="ml-1 text-sm">{attraction.rating}</span>
                  </div>
                </div>
                <div className="flex flex-wrap gap-y-2 gap-x-4 text-sm text-muted-foreground mb-3">
                  <div className="flex items-center gap-1">
                    <MapPin className="h-4 w-4" />
                    <span>{attraction.location}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Clock className="h-4 w-4" />
                    <span>{attraction.duration}</span>
                  </div>
                </div>
                <p className="text-muted-foreground mb-4 line-clamp-2">{attraction.description}</p>
                <Button asChild variant="outline" size="sm">
                  <Link to={`/discover/${attraction.id}`}>
                    Learn More
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
        
        {filteredAttractions.length === 0 && (
          <div className="text-center py-16">
            <h3 className="text-xl font-semibold mb-2">No attractions found</h3>
            <p className="text-muted-foreground">Try adjusting your search criteria or explore a different category.</p>
          </div>
        )}
      </section>
      
      {/* Plan Your Trip Section */}
      <section className="py-12 bg-accent/20">
        <div className="container">
          <div className="bg-card rounded-xl overflow-hidden border shadow-sm">
            <div className="grid grid-cols-1 md:grid-cols-2">
              <div className="p-8 flex flex-col justify-center">
                <h2 className="text-3xl font-bold mb-4">Ready to Explore?</h2>
                <p className="text-lg text-muted-foreground mb-6">
                  Create your custom itinerary and make the most of your visit to Nashik.
                </p>
                <div className="flex flex-col sm:flex-row gap-3">
                  <Button asChild size="lg">
                    <Link to="/plan-trip">
                      Plan My Trip
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Link>
                  </Button>
                  <Button asChild variant="outline" size="lg">
                    <Link to="/hotels">
                      Find Accommodation
                    </Link>
                  </Button>
                </div>
              </div>
              <div className="h-64 md:h-auto">
                <img 
                  src="https://images.unsplash.com/photo-1605345981660-b1ae6516d2e6?q=80&w=1974&auto=format&fit=crop" 
                  alt="Plan your trip to Nashik" 
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <Footer />
    </div>
  );
};

export default Discover;
