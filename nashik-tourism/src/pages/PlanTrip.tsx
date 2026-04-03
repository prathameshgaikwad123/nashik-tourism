
import { useState } from "react";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { DatePicker } from "@/components/date-picker";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Calendar, MapPin, Users, CalendarClock, Hotel } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const PlanTrip = () => {
  const [tripType, setTripType] = useState("day-trip");
  const { toast } = useToast();
  
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    toast({
      title: "Trip plan submitted!",
      description: "We'll contact you soon with your custom itinerary.",
    });
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="relative h-[30vh] sm:h-[40vh] md:h-[50vh]">
          <img 
            src="https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=2070&auto=format&fit=crop"
            alt="Scenic view of Nashik vineyards and mountains" 
            className="w-full h-full object-cover" 
          />
          <div className="absolute inset-0 bg-black/40 flex items-center">
            <div className="container px-4 sm:px-6">
              <h1 className="text-2xl sm:text-3xl md:text-5xl font-bold text-white mb-2 sm:mb-4">Plan Your Nashik Adventure</h1>
              <p className="text-base sm:text-lg text-white/90 max-w-2xl">
                Customize your perfect trip with our personalized itinerary planner
              </p>
            </div>
          </div>
        </section>

        {/* Trip Planner Section */}
        <section className="container py-8 sm:py-12 px-4 sm:px-6">
          <div className="max-w-4xl mx-auto">
            <Tabs defaultValue="day-trip" onValueChange={setTripType} className="w-full">
              <TabsList className="grid grid-cols-3 mb-6 sm:mb-8 w-full">
                <TabsTrigger value="day-trip" className="text-xs sm:text-sm">Day Trip</TabsTrigger>
                <TabsTrigger value="weekend" className="text-xs sm:text-sm">Weekend Getaway</TabsTrigger>
                <TabsTrigger value="custom" className="text-xs sm:text-sm">Custom Plan</TabsTrigger>
              </TabsList>
              
              <Card className="border shadow-md">
                <CardHeader>
                  <CardTitle>
                    {tripType === "day-trip" && "Day Trip Planner"}
                    {tripType === "weekend" && "Weekend Getaway Planner"}
                    {tripType === "custom" && "Custom Trip Planner"}
                  </CardTitle>
                  <CardDescription>
                    {tripType === "day-trip" && "Perfect for quick visits to Nashik's top attractions"}
                    {tripType === "weekend" && "Ideal for a 2-3 day relaxing experience"}
                    {tripType === "custom" && "Design your own perfect Nashik adventure"}
                  </CardDescription>
                </CardHeader>
                
                <CardContent>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                      <div className="space-y-2">
                        <Label htmlFor="name">Full Name</Label>
                        <Input id="name" placeholder="Your name" required />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="email">Email Address</Label>
                        <Input id="email" type="email" placeholder="your.email@example.com" required />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="phone">Phone Number</Label>
                        <Input id="phone" placeholder="+91 98765 43210" />
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="date">Travel Date</Label>
                        <div className="relative">
                          <DatePicker />
                        </div>
                      </div>
                      
                      <div className="space-y-2">
                        <Label htmlFor="people">Number of People</Label>
                        <Select defaultValue="2">
                          <SelectTrigger id="people">
                            <SelectValue placeholder="Select" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="1">1 Person</SelectItem>
                            <SelectItem value="2">2 People</SelectItem>
                            <SelectItem value="3-5">3-5 People</SelectItem>
                            <SelectItem value="6-10">6-10 People</SelectItem>
                            <SelectItem value="10+">More than 10</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      
                      {tripType !== "day-trip" && (
                        <div className="space-y-2">
                          <Label htmlFor="nights">Number of Nights</Label>
                          <Select defaultValue="2">
                            <SelectTrigger id="nights">
                              <SelectValue placeholder="Select" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="1">1 Night</SelectItem>
                              <SelectItem value="2">2 Nights</SelectItem>
                              <SelectItem value="3">3 Nights</SelectItem>
                              <SelectItem value="4-7">4-7 Nights</SelectItem>
                              <SelectItem value="8+">More than a week</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      )}
                      
                      <div className="space-y-2 sm:col-span-2">
                        <Label htmlFor="interests">Interests (Select all that apply)</Label>
                        <div className="grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-3 gap-2 pt-2">
                          <Button type="button" variant="outline" className="justify-start">
                            <MapPin className="mr-2 h-4 w-4" /> Wineries
                          </Button>
                          <Button type="button" variant="outline" className="justify-start">
                            <MapPin className="mr-2 h-4 w-4" /> Religious Sites
                          </Button>
                          <Button type="button" variant="outline" className="justify-start">
                            <MapPin className="mr-2 h-4 w-4" /> Historical Places
                          </Button>
                          <Button type="button" variant="outline" className="justify-start">
                            <MapPin className="mr-2 h-4 w-4" /> Nature & Hiking
                          </Button>
                          <Button type="button" variant="outline" className="justify-start">
                            <MapPin className="mr-2 h-4 w-4" /> Local Cuisine
                          </Button>
                          <Button type="button" variant="outline" className="justify-start">
                            <MapPin className="mr-2 h-4 w-4" /> Shopping
                          </Button>
                        </div>
                      </div>
                      
                      <div className="sm:col-span-2">
                        <Label htmlFor="notes">Additional Requirements</Label>
                        <Input id="notes" placeholder="Any special requests or needs?" className="mt-2" />
                      </div>
                    </div>
                    
                    <Button type="submit" className="w-full">
                      Create My Itinerary
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </Tabs>
          </div>
        </section>
        
        {/* Popular Itinerary Templates */}
        <section className="bg-muted/50 py-8 sm:py-12 px-4 sm:px-6">
          <div className="container">
            <h2 className="text-xl sm:text-2xl font-bold mb-6 sm:mb-8 text-center">Popular Itinerary Templates</h2>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
              <Card className="card-hover">
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <CalendarClock className="mr-2 h-5 w-5 text-primary" />
                    Nashik in a Day
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4 text-sm sm:text-base">Perfect for travelers with limited time. Visit key highlights including a winery and sacred sites.</p>
                  <ul className="space-y-2 text-xs sm:text-sm">
                    <li className="flex items-start">
                      <span className="font-medium mr-2">Morning:</span> Sula Vineyards tour & tasting
                    </li>
                    <li className="flex items-start">
                      <span className="font-medium mr-2">Afternoon:</span> Trimbakeshwar Temple visit
                    </li>
                    <li className="flex items-start">
                      <span className="font-medium mr-2">Evening:</span> Sunset at Soma Vineyards
                    </li>
                  </ul>
                </CardContent>
                <CardFooter>
                  <Button variant="outline" className="w-full">See Details</Button>
                </CardFooter>
              </Card>
              
              <Card className="card-hover">
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <Users className="mr-2 h-5 w-5 text-primary" />
                    Weekend Family Escape
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4 text-sm sm:text-base">A balanced 2-day trip with activities for all ages, including nature, culture and relaxation.</p>
                  <ul className="space-y-2 text-xs sm:text-sm">
                    <li className="flex items-start">
                      <span className="font-medium mr-2">Day 1:</span> Vineyards & Pandavleni Caves
                    </li>
                    <li className="flex items-start">
                      <span className="font-medium mr-2">Evening:</span> Local cuisine dinner
                    </li>
                    <li className="flex items-start">
                      <span className="font-medium mr-2">Day 2:</span> Temple tour & shopping
                    </li>
                  </ul>
                </CardContent>
                <CardFooter>
                  <Button variant="outline" className="w-full">See Details</Button>
                </CardFooter>
              </Card>
              
              <Card className="card-hover mt-4 sm:mt-0">
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <Hotel className="mr-2 h-5 w-5 text-primary" />
                    Wine & Wellness Retreat
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4 text-sm sm:text-base">A 3-day immersive experience combining wine tasting, spa treatments, and spiritual activities.</p>
                  <ul className="space-y-2 text-xs sm:text-sm">
                    <li className="flex items-start">
                      <span className="font-medium mr-2">Day 1:</span> Wine tour & tasting
                    </li>
                    <li className="flex items-start">
                      <span className="font-medium mr-2">Day 2:</span> Spa day & meditation
                    </li>
                    <li className="flex items-start">
                      <span className="font-medium mr-2">Day 3:</span> Sacred sites & river walk
                    </li>
                  </ul>
                </CardContent>
                <CardFooter>
                  <Button variant="outline" className="w-full">See Details</Button>
                </CardFooter>
              </Card>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default PlanTrip;
