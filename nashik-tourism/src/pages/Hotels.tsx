import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { MapPin, Star, Wifi, Coffee, Car, Users } from "lucide-react";
import { DatePicker } from "@/components/date-picker";

const Hotels = () => {
  const featuredHotels = [
    {
      id: 1,
      name: "Sula Vineyard Resort",
      image: "https://images.unsplash.com/photo-1566073771259-6a8506099945?q=80&w=2070&auto=format&fit=crop",
      location: "Sula Vineyards, Nashik",
      price: "₹7,500",
      rating: 4.8,
      amenities: ["Vineyard views", "Pool", "Restaurant", "Spa"]
    },
    {
      id: 2,
      name: "Riverside Grand Hotel",
      image: "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?q=80&w=2070&auto=format&fit=crop",
      location: "Godavari Riverfront, Nashik",
      price: "₹5,200",
      rating: 4.5,
      amenities: ["River view", "Restaurant", "Gym", "Free Wi-Fi"]
    },
    {
      id: 3,
      name: "Heritage Inn",
      image: "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?q=80&w=2070&auto=format&fit=crop",
      location: "Panchvati, Nashik",
      price: "₹3,800",
      rating: 4.3,
      amenities: ["Traditional decor", "Temple proximity", "Restaurant", "Tour desk"]
    },
    {
      id: 4,
      name: "City Center Suites",
      image: "https://images.unsplash.com/photo-1618773928121-c32242e63f39?q=80&w=2070&auto=format&fit=crop",
      location: "College Road, Nashik",
      price: "₹4,500",
      rating: 4.2,
      amenities: ["City view", "Restaurant", "Fitness center", "Conference rooms"]
    },
    {
      id: 5,
      name: "Trimbak Valley Resort",
      image: "https://images.unsplash.com/photo-1586611292717-f828b167408c?q=80&w=2070&auto=format&fit=crop",
      location: "Trimbakeshwar Road, Nashik",
      price: "₹6,200",
      rating: 4.6,
      amenities: ["Mountain views", "Outdoor activities", "Restaurant", "Spa"]
    },
    {
      id: 6,
      name: "Wine Country Lodge",
      image: "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?q=80&w=2070&auto=format&fit=crop",
      location: "Gangapur Road, Nashik",
      price: "₹4,800",
      rating: 4.4,
      amenities: ["Vineyard tours", "Wine tasting", "Restaurant", "Pool"]
    }
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <section className="relative h-[40vh] md:h-[50vh]">
          <img 
            src="https://images.unsplash.com/photo-1571896349842-33c89424de2d?q=80&w=2080&auto=format&fit=crop"
            alt="Luxury hotel room with vineyard view in Nashik" 
            className="w-full h-full object-cover" 
          />
          <div className="absolute inset-0 bg-black/40 flex items-center">
            <div className="container">
              <h1 className="text-3xl md:text-5xl font-bold text-white mb-4">Book Hotels in Nashik</h1>
              <p className="text-lg text-white/90 max-w-2xl">
                Find your perfect stay from luxury resorts to cozy vineyard stays
              </p>
            </div>
          </div>
        </section>

        <section className="container py-12">
          <Card className="mb-12 border">
            <CardHeader>
              <CardTitle>Find Your Perfect Stay</CardTitle>
              <CardDescription>Search for accommodations in and around Nashik</CardDescription>
            </CardHeader>
            <CardContent>
              <form className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="location">Location</Label>
                    <div className="relative">
                      <MapPin className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                      <Input id="location" placeholder="All of Nashik" className="pl-8" />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="check-in">Check-in Date</Label>
                    <DatePicker />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="check-out">Check-out Date</Label>
                    <DatePicker />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="guests">Guests</Label>
                    <div className="relative">
                      <Users className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                      <Input id="guests" placeholder="2 Adults, 0 Children" className="pl-8" />
                    </div>
                  </div>
                </div>
                
                <Button type="submit" className="w-full md:w-auto">Search Hotels</Button>
              </form>
            </CardContent>
          </Card>

          <div className="mb-10">
            <h2 className="text-2xl font-bold mb-6">Featured Hotels & Stays</h2>
            <Tabs defaultValue="all">
              <TabsList className="mb-6">
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="luxury">Luxury</TabsTrigger>
                <TabsTrigger value="vineyard">Vineyard Stays</TabsTrigger>
                <TabsTrigger value="budget">Budget-Friendly</TabsTrigger>
              </TabsList>
              
              <TabsContent value="all" className="mt-0">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {featuredHotels.map(hotel => (
                    <Card key={hotel.id} className="overflow-hidden card-hover">
                      <div className="h-48 overflow-hidden">
                        <img 
                          src={hotel.image} 
                          alt={`${hotel.name} in Nashik`}
                          className="w-full h-full object-cover transition-transform hover:scale-105 duration-300"
                        />
                      </div>
                      <CardHeader>
                        <CardTitle className="text-lg">{hotel.name}</CardTitle>
                        <CardDescription className="flex items-center">
                          <MapPin className="h-3.5 w-3.5 mr-1" /> {hotel.location}
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-center mb-3">
                          {[...Array(5)].map((_, i) => (
                            <Star 
                              key={i}
                              className={`w-4 h-4 ${i < Math.floor(hotel.rating) ? "text-primary fill-primary" : "text-muted-foreground"}`}
                            />
                          ))}
                          <span className="ml-2 text-sm">{hotel.rating}/5</span>
                        </div>
                        <div className="flex flex-wrap gap-2 mb-4">
                          {hotel.amenities.map(amenity => (
                            <span key={amenity} className="text-xs bg-muted px-2 py-1 rounded-full">
                              {amenity}
                            </span>
                          ))}
                        </div>
                        <p className="font-semibold text-lg">{hotel.price} <span className="text-sm font-normal text-muted-foreground">per night</span></p>
                      </CardContent>
                      <CardFooter>
                        <Button variant="outline" className="w-full">View Details</Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              </TabsContent>
              
              <TabsContent value="luxury" className="mt-0">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {featuredHotels
                    .filter(h => parseInt(h.price.replace("₹", "").replace(",", "")) > 5000)
                    .map(hotel => (
                    <Card key={hotel.id} className="overflow-hidden card-hover">
                      <div className="h-48 overflow-hidden">
                        <img 
                          src={hotel.image} 
                          alt={`${hotel.name} in Nashik`}
                          className="w-full h-full object-cover transition-transform hover:scale-105 duration-300"
                        />
                      </div>
                      <CardHeader>
                        <CardTitle className="text-lg">{hotel.name}</CardTitle>
                        <CardDescription className="flex items-center">
                          <MapPin className="h-3.5 w-3.5 mr-1" /> {hotel.location}
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-center mb-3">
                          {[...Array(5)].map((_, i) => (
                            <Star 
                              key={i}
                              className={`w-4 h-4 ${i < Math.floor(hotel.rating) ? "text-primary fill-primary" : "text-muted-foreground"}`}
                            />
                          ))}
                          <span className="ml-2 text-sm">{hotel.rating}/5</span>
                        </div>
                        <div className="flex flex-wrap gap-2 mb-4">
                          {hotel.amenities.map(amenity => (
                            <span key={amenity} className="text-xs bg-muted px-2 py-1 rounded-full">
                              {amenity}
                            </span>
                          ))}
                        </div>
                        <p className="font-semibold text-lg">{hotel.price} <span className="text-sm font-normal text-muted-foreground">per night</span></p>
                      </CardContent>
                      <CardFooter>
                        <Button variant="outline" className="w-full">View Details</Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              </TabsContent>
              
              <TabsContent value="vineyard" className="mt-0">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {featuredHotels
                    .filter(h => h.name.toLowerCase().includes("vineyard") || h.name.toLowerCase().includes("wine"))
                    .map(hotel => (
                    <Card key={hotel.id} className="overflow-hidden card-hover">
                      <div className="h-48 overflow-hidden">
                        <img 
                          src={hotel.image} 
                          alt={`${hotel.name} in Nashik`}
                          className="w-full h-full object-cover transition-transform hover:scale-105 duration-300"
                        />
                      </div>
                      <CardHeader>
                        <CardTitle className="text-lg">{hotel.name}</CardTitle>
                        <CardDescription className="flex items-center">
                          <MapPin className="h-3.5 w-3.5 mr-1" /> {hotel.location}
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-center mb-3">
                          {[...Array(5)].map((_, i) => (
                            <Star 
                              key={i}
                              className={`w-4 h-4 ${i < Math.floor(hotel.rating) ? "text-primary fill-primary" : "text-muted-foreground"}`}
                            />
                          ))}
                          <span className="ml-2 text-sm">{hotel.rating}/5</span>
                        </div>
                        <div className="flex flex-wrap gap-2 mb-4">
                          {hotel.amenities.map(amenity => (
                            <span key={amenity} className="text-xs bg-muted px-2 py-1 rounded-full">
                              {amenity}
                            </span>
                          ))}
                        </div>
                        <p className="font-semibold text-lg">{hotel.price} <span className="text-sm font-normal text-muted-foreground">per night</span></p>
                      </CardContent>
                      <CardFooter>
                        <Button variant="outline" className="w-full">View Details</Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              </TabsContent>
              
              <TabsContent value="budget" className="mt-0">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {featuredHotels
                    .filter(h => parseInt(h.price.replace("₹", "").replace(",", "")) < 5000)
                    .map(hotel => (
                    <Card key={hotel.id} className="overflow-hidden card-hover">
                      <div className="h-48 overflow-hidden">
                        <img 
                          src={hotel.image} 
                          alt={`${hotel.name} in Nashik`}
                          className="w-full h-full object-cover transition-transform hover:scale-105 duration-300"
                        />
                      </div>
                      <CardHeader>
                        <CardTitle className="text-lg">{hotel.name}</CardTitle>
                        <CardDescription className="flex items-center">
                          <MapPin className="h-3.5 w-3.5 mr-1" /> {hotel.location}
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-center mb-3">
                          {[...Array(5)].map((_, i) => (
                            <Star 
                              key={i}
                              className={`w-4 h-4 ${i < Math.floor(hotel.rating) ? "text-primary fill-primary" : "text-muted-foreground"}`}
                            />
                          ))}
                          <span className="ml-2 text-sm">{hotel.rating}/5</span>
                        </div>
                        <div className="flex flex-wrap gap-2 mb-4">
                          {hotel.amenities.map(amenity => (
                            <span key={amenity} className="text-xs bg-muted px-2 py-1 rounded-full">
                              {amenity}
                            </span>
                          ))}
                        </div>
                        <p className="font-semibold text-lg">{hotel.price} <span className="text-sm font-normal text-muted-foreground">per night</span></p>
                      </CardContent>
                      <CardFooter>
                        <Button variant="outline" className="w-full">View Details</Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              </TabsContent>
            </Tabs>
          </div>

          <div className="bg-muted rounded-lg p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div>
              <h3 className="text-xl font-bold mb-2">Need help finding the perfect accommodation?</h3>
              <p className="text-muted-foreground">Our local experts can help you find the best stay for your budget and preferences.</p>
            </div>
            <Button size="lg" className="whitespace-nowrap">Contact Us</Button>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default Hotels;
