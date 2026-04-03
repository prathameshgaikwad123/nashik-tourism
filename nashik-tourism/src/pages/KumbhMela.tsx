
import { useState } from "react";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { Calendar, Clock, MapPin, Info, Download, AlertTriangle, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const KeyDates = [
  { event: "Kumbh Mela Begins", date: "April 8, 2027", description: "Opening ceremonies and first auspicious bathing day" },
  { event: "Shahi Snan (Royal Bath)", date: "April 12, 2027", description: "First major bathing day for sadhus and pilgrims" },
  { event: "Mauni Amavasya", date: "April 20, 2027", description: "Most auspicious bathing day during Kumbh Mela" },
  { event: "Basant Panchami Snan", date: "May 3, 2027", description: "Bathing day celebrating the arrival of spring" },
  { event: "Maghi Poornima Snan", date: "May 17, 2027", description: "Full moon bathing day of significant importance" },
  { event: "Maha Shivratri", date: "May 29, 2027", description: "Final major bathing day dedicated to Lord Shiva" },
  { event: "Kumbh Mela Concludes", date: "June 8, 2027", description: "Closing ceremonies and final rituals" },
];

const Itineraries = [
  {
    title: "1-Day Essential Kumbh Experience",
    description: "Perfect for those with limited time who want to experience the essence of Kumbh Mela.",
    activities: [
      { time: "6:00 AM", activity: "Visit Ramkund for early morning aarti" },
      { time: "8:00 AM", activity: "Attend a spiritual discourse at the main pandal" },
      { time: "11:00 AM", activity: "Explore the Sadhus' akharas" },
      { time: "1:00 PM", activity: "Lunch at the community kitchen (langar)" },
      { time: "3:00 PM", activity: "Visit exhibition areas and cultural performances" },
      { time: "5:00 PM", activity: "Evening aarti at Godavari River" },
      { time: "7:00 PM", activity: "Experience the vibrant night atmosphere and light shows" },
    ]
  },
  {
    title: "3-Day Spiritual Immersion",
    description: "A deeper dive into the spiritual aspects of the Kumbh Mela with more time for reflection.",
    activities: [
      { time: "Day 1", activity: "Morning bathing rituals, visit to main temples, evening aarti" },
      { time: "Day 2", activity: "Spiritual discourses, meditation sessions, explore different akharas" },
      { time: "Day 3", activity: "Visit nearby sacred sites, participate in community service, closing ceremonies" },
    ]
  },
  {
    title: "5-Day Complete Kumbh Journey",
    description: "The full Kumbh experience with time to explore all aspects of this spiritual gathering.",
    activities: [
      { time: "Day 1", activity: "Arrival and orientation, evening ceremonies" },
      { time: "Day 2", activity: "Main bathing rituals and temple visits" },
      { time: "Day 3", activity: "Spiritual discourses and meditation retreats" },
      { time: "Day 4", activity: "Cultural programs and visiting different sectarian camps" },
      { time: "Day 5", activity: "Final sacred bath, closing rituals, and reflection" },
    ]
  },
];

const KumbhMela = () => {
  const [selectedTab, setSelectedTab] = useState("overview");

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative h-[60vh] overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: "url('https://images.unsplash.com/photo-1616680214603-c5ab1a9df3f7?q=80&w=2070&auto=format&fit=crop')",
          }}
        />
        <div className="absolute inset-0 hero-gradient" />
        <div className="container relative z-10 h-full flex flex-col justify-center items-start text-white">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">
            Kumbh Mela 2027
          </h1>
          <p className="text-xl mb-6 max-w-2xl">
            The world's largest spiritual gathering, held once every 12 years in Nashik.
          </p>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              <span>April 8 - June 8, 2027</span>
            </div>
            <div className="flex items-center gap-2">
              <MapPin className="h-5 w-5" />
              <span>Nashik, Maharashtra</span>
            </div>
          </div>
        </div>
      </section>
      
      {/* Main Content */}
      <section className="py-16 container">
        <Tabs defaultValue="overview" value={selectedTab} onValueChange={setSelectedTab}>
          <TabsList className="grid w-full grid-cols-2 md:grid-cols-4 mb-8">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="key-dates">Key Dates</TabsTrigger>
            <TabsTrigger value="planning-guide">Planning Guide</TabsTrigger>
            <TabsTrigger value="itineraries">Sample Itineraries</TabsTrigger>
          </TabsList>
          
          <TabsContent value="overview" className="mt-0">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="col-span-2">
                <h2 className="text-3xl font-bold mb-6">About Kumbh Mela</h2>
                <div className="prose prose-lg max-w-none dark:prose-invert">
                  <p>
                    Kumbh Mela is the largest peaceful gathering of pilgrims on earth, during which participants bathe or take a dip in a sacred river. It is a religious pilgrimage that is celebrated four times over the course of 12 years, the site of the observance rotating between four pilgrimage places on four sacred rivers:
                  </p>
                  <ul>
                    <li>Prayagraj (Ganges-Yamuna-Sarasvati rivers confluence)</li>
                    <li>Haridwar (Ganges)</li>
                    <li>Ujjain (Shipra)</li>
                    <li>Nashik (Godavari)</li>
                  </ul>
                  <p>
                    In 2027, this grand celebration returns to Nashik, attracting millions of devotees, sadhus (holy men), and tourists from around the world.
                  </p>
                  <h3>Historical Significance</h3>
                  <p>
                    According to Hindu mythology, Kumbh Mela commemorates the time when the gods and demons fought over the sacred pot (kumbh) of amrit (nectar of immortality). During this struggle, drops of the nectar fell at the four places where the Kumbh Mela is now held.
                  </p>
                  <p>
                    The Nashik Kumbh Mela, also known as Sinhastha, occurs when Jupiter is in Leo (Simha Rashi) and the Sun and Moon are in Cancer (Karka Rashi). The last Nashik Kumbh Mela was held in 2015, and the next one in 2027 is expected to draw even larger crowds.
                  </p>
                </div>
                
                <div className="mt-10">
                  <h3 className="text-2xl font-bold mb-4">Spiritual Significance</h3>
                  <div className="prose prose-lg max-w-none dark:prose-invert">
                    <p>
                      For devotees, taking a holy dip in the Godavari River during Kumbh Mela is believed to cleanse one of all sins and break the cycle of rebirth. It's a time for spiritual reflection, seeking blessings, and immersing oneself in the divine atmosphere.
                    </p>
                    <p>
                      The gathering also provides a rare opportunity to meet and learn from various sadhus and spiritual leaders who normally live in seclusion. Many devotees consider this interaction as important as the ritual bath itself.
                    </p>
                  </div>
                </div>
                
                <div className="mt-10">
                  <h3 className="text-2xl font-bold mb-4">Cultural Experience</h3>
                  <div className="prose prose-lg max-w-none dark:prose-invert">
                    <p>
                      Beyond its religious significance, Kumbh Mela is a spectacular cultural festival. Visitors can witness colorful processions, religious discourses, devotional music, and traditional performances. The temporary city that springs up to accommodate millions features diverse traditions from across India.
                    </p>
                    <p>
                      For photographers and cultural enthusiasts, the festival offers unparalleled opportunities to document one of humanity's most extraordinary gatherings.
                    </p>
                  </div>
                </div>
              </div>
              
              <div>
                <div className="bg-accent/30 rounded-lg p-6 mb-6">
                  <h3 className="text-xl font-semibold mb-4">Quick Facts</h3>
                  <ul className="space-y-4">
                    <li className="flex gap-3">
                      <Calendar className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                      <div>
                        <span className="font-medium">Duration:</span>
                        <p className="text-muted-foreground">2 months (April 8 - June 8, 2027)</p>
                      </div>
                    </li>
                    <li className="flex gap-3">
                      <MapPin className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                      <div>
                        <span className="font-medium">Location:</span>
                        <p className="text-muted-foreground">Banks of Godavari River, Nashik, Maharashtra</p>
                      </div>
                    </li>
                    <li className="flex gap-3">
                      <Info className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                      <div>
                        <span className="font-medium">Expected Visitors:</span>
                        <p className="text-muted-foreground">30-50 million pilgrims</p>
                      </div>
                    </li>
                    <li className="flex gap-3">
                      <Clock className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                      <div>
                        <span className="font-medium">Main Bathing Dates:</span>
                        <p className="text-muted-foreground">April 12, April 20, May 3, May 17, May 29</p>
                      </div>
                    </li>
                  </ul>
                </div>
                
                <div className="rounded-lg overflow-hidden mb-6">
                  <img 
                    src="https://images.unsplash.com/photo-1598343675812-c657ddcbcd11?q=80&w=1974&auto=format&fit=crop" 
                    alt="Kumbh Mela ceremony" 
                    className="w-full"
                  />
                </div>
                
                <div className="bg-accent/30 rounded-lg p-6">
                  <h3 className="text-xl font-semibold mb-4">Plan Your Visit</h3>
                  <p className="text-muted-foreground mb-4">
                    Start planning your Kumbh Mela journey with our comprehensive trip planner.
                  </p>
                  <Button asChild className="w-full">
                    <Link to="/plan-trip">
                      Create Kumbh Mela Itinerary
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Link>
                  </Button>
                </div>
              </div>
            </div>
          </TabsContent>
          
          <TabsContent value="key-dates" className="mt-0">
            <h2 className="text-3xl font-bold mb-6">Key Dates & Events</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {KeyDates.map((item, index) => (
                <div 
                  key={index} 
                  className="bg-card rounded-lg border p-6 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-center gap-2 text-primary mb-2">
                    <Calendar className="h-5 w-5" />
                    <h3 className="font-semibold">{item.date}</h3>
                  </div>
                  <h4 className="text-xl font-semibold mb-2">{item.event}</h4>
                  <p className="text-muted-foreground">{item.description}</p>
                </div>
              ))}
            </div>
            
            <div className="mt-10 bg-accent/30 rounded-lg p-6">
              <div className="flex items-start gap-4">
                <Info className="h-6 w-6 text-primary flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-xl font-semibold mb-2">Important Note</h3>
                  <p className="text-muted-foreground">
                    These dates are based on traditional Hindu astrological calculations and may be subject to minor adjustments. We recommend confirming the final schedule closer to the event.
                  </p>
                </div>
              </div>
            </div>
            
            <div className="mt-6 text-center">
              <Button asChild>
                <Link to="/plan-trip">
                  Plan Your Visit Around These Dates
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
          </TabsContent>
          
          <TabsContent value="planning-guide" className="mt-0">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="col-span-2">
                <h2 className="text-3xl font-bold mb-6">Kumbh Mela Planning Guide</h2>
                
                <div className="mb-8">
                  <h3 className="text-2xl font-bold mb-4">Before You Go</h3>
                  <div className="prose prose-lg max-w-none dark:prose-invert">
                    <h4>Accommodation</h4>
                    <p>
                      Book your accommodation well in advance, at least 6-8 months before the event. Options include:
                    </p>
                    <ul>
                      <li><strong>Luxury tented camps:</strong> Premium experience with amenities</li>
                      <li><strong>Hotels and guesthouses:</strong> Limited availability in Nashik city</li>
                      <li><strong>Ashrams:</strong> Basic accommodation with spiritual environment</li>
                      <li><strong>Government tent cities:</strong> Budget-friendly options set up specifically for the event</li>
                    </ul>
                    
                    <h4>Travel Arrangements</h4>
                    <p>
                      The nearest airports are in Mumbai and Pune, with onward travel to Nashik by road or rail:
                    </p>
                    <ul>
                      <li><strong>By Air:</strong> Fly to Mumbai (185 km) or Pune (214 km)</li>
                      <li><strong>By Train:</strong> Regular services connect Nashik to major cities</li>
                      <li><strong>By Road:</strong> Well-connected highways from Mumbai, Pune, and other cities</li>
                    </ul>
                    <p>
                      During Kumbh Mela, special transportation services are usually available, but advance booking is recommended.
                    </p>
                    
                    <h4>Essential Documents</h4>
                    <ul>
                      <li>Valid ID proof</li>
                      <li>Travel insurance</li>
                      <li>Accommodation confirmation</li>
                      <li>Emergency contact information</li>
                      <li>Basic medical information card</li>
                    </ul>
                  </div>
                </div>
                
                <div className="mb-8">
                  <h3 className="text-2xl font-bold mb-4">During Your Visit</h3>
                  <div className="prose prose-lg max-w-none dark:prose-invert">
                    <h4>What to Wear</h4>
                    <ul>
                      <li>Modest, comfortable clothing (shoulders and knees covered)</li>
                      <li>Lightweight, breathable fabrics</li>
                      <li>Hat and sunglasses for sun protection</li>
                      <li>Comfortable walking shoes that can get wet</li>
                      <li>Light jacket or shawl for evenings</li>
                    </ul>
                    
                    <h4>What to Bring</h4>
                    <ul>
                      <li>Refillable water bottle</li>
                      <li>Hand sanitizer and wet wipes</li>
                      <li>Basic first aid kit</li>
                      <li>Mosquito repellent</li>
                      <li>Power bank for mobile devices</li>
                      <li>Small backpack for daily essentials</li>
                      <li>Quick-dry towel</li>
                    </ul>
                    
                    <h4>Etiquette & Cultural Sensitivity</h4>
                    <ul>
                      <li>Ask permission before photographing sadhus or ceremonies</li>
                      <li>Remove shoes before entering temples or sacred areas</li>
                      <li>Avoid touching holy men or women</li>
                      <li>Participate respectfully in ceremonies</li>
                      <li>Be mindful of noise levels during religious discourses</li>
                    </ul>
                  </div>
                </div>
              </div>
              
              <div>
                <div className="bg-nashik-purple/10 rounded-lg p-6 mb-6">
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="h-6 w-6 text-nashik-purple flex-shrink-0 mt-0.5" />
                    <div>
                      <h3 className="text-xl font-semibold mb-2">Safety Tips</h3>
                      <ul className="space-y-3">
                        <li className="flex items-start gap-2">
                          <span className="text-nashik-purple font-bold">•</span>
                          <p className="text-muted-foreground">Stay hydrated and protect yourself from the sun</p>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-nashik-purple font-bold">•</span>
                          <p className="text-muted-foreground">Keep valuables secure and minimize carrying cash</p>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-nashik-purple font-bold">•</span>
                          <p className="text-muted-foreground">Be aware of your surroundings in crowded areas</p>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-nashik-purple font-bold">•</span>
                          <p className="text-muted-foreground">Use only designated bathing areas</p>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-nashik-purple font-bold">•</span>
                          <p className="text-muted-foreground">Follow instructions from event authorities</p>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-nashik-purple font-bold">•</span>
                          <p className="text-muted-foreground">Have a meeting point in case your group gets separated</p>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <div className="bg-card rounded-lg border p-6 mb-6">
                  <h3 className="text-xl font-semibold mb-3">Health Precautions</h3>
                  <ul className="space-y-3">
                    <li className="flex items-start gap-2">
                      <span className="text-primary font-bold">•</span>
                      <p className="text-muted-foreground">Carry any necessary prescription medications</p>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-primary font-bold">•</span>
                      <p className="text-muted-foreground">Drink only bottled or purified water</p>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-primary font-bold">•</span>
                      <p className="text-muted-foreground">Use sunscreen and stay in shade during peak hours</p>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-primary font-bold">•</span>
                      <p className="text-muted-foreground">Wash hands frequently or use sanitizer</p>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-primary font-bold">•</span>
                      <p className="text-muted-foreground">Know the location of medical centers at the event</p>
                    </li>
                  </ul>
                </div>
                
                <div className="bg-accent/30 rounded-lg p-6">
                  <h3 className="text-xl font-semibold mb-3">Planning Resources</h3>
                  <div className="space-y-4">
                    <Button variant="outline" className="w-full flex justify-between items-center">
                      <span>Kumbh Mela Map</span>
                      <Download className="h-4 w-4" />
                    </Button>
                    <Button variant="outline" className="w-full flex justify-between items-center">
                      <span>Event Schedule PDF</span>
                      <Download className="h-4 w-4" />
                    </Button>
                    <Button variant="outline" className="w-full flex justify-between items-center">
                      <span>Visitor Guidelines</span>
                      <Download className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </TabsContent>
          
          <TabsContent value="itineraries" className="mt-0">
            <h2 className="text-3xl font-bold mb-6">Sample Itineraries</h2>
            
            <div className="grid grid-cols-1 gap-8">
              {Itineraries.map((itinerary, index) => (
                <div key={index} className="bg-card rounded-lg border overflow-hidden">
                  <div className="bg-primary/5 p-6">
                    <h3 className="text-2xl font-semibold mb-2">{itinerary.title}</h3>
                    <p className="text-muted-foreground">{itinerary.description}</p>
                  </div>
                  <div className="p-6">
                    <h4 className="font-medium mb-4">Suggested Schedule:</h4>
                    <div className="space-y-4">
                      {itinerary.activities.map((activity, actIndex) => (
                        <div key={actIndex} className="flex gap-4">
                          <div className="w-20 flex-shrink-0 font-medium">{activity.time}</div>
                          <div>{activity.activity}</div>
                        </div>
                      ))}
                    </div>
                    <div className="mt-6 flex justify-end">
                      <Button asChild variant="outline">
                        <Link to="/plan-trip">
                          Customize This Itinerary
                          <ArrowRight className="ml-2 h-4 w-4" />
                        </Link>
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-10 bg-primary/5 rounded-lg p-6">
              <div className="flex items-start gap-4">
                <Info className="h-6 w-6 text-primary flex-shrink-0 mt-1" />
                <div>
                  <h3 className="text-xl font-semibold mb-2">Create Your Own Experience</h3>
                  <p className="text-muted-foreground mb-4">
                    These sample itineraries are just starting points. Use our interactive trip planner to create a customized schedule based on your interests, time constraints, and spiritual objectives.
                  </p>
                  <Button asChild>
                    <Link to="/plan-trip">
                      Plan Your Custom Kumbh Mela Journey
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Link>
                  </Button>
                </div>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </section>
      
      <Footer />
    </div>
  );
};

export default KumbhMela;
