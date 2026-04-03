
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Clock, User, Calendar, ArrowRight, Search } from "lucide-react";
import { Link } from "react-router-dom";

const Blog = () => {
  const blogPosts = [
    {
      id: 1,
      title: "Top 10 Wineries to Visit in Nashik",
      excerpt: "Discover the best vineyards and wine tasting experiences in India's wine capital.",
      category: "Wine Tourism",
      image: "https://images.unsplash.com/photo-1560830889-5c5c15827b84?q=80&w=2070&auto=format&fit=crop",
      author: "Vineeta Sharma",
      date: "April 10, 2025",
      readTime: "8 min read"
    },
    {
      id: 2,
      title: "The Sacred Sites of Nashik: A Spiritual Journey",
      excerpt: "Explore the temples, ghats and religious significance of this ancient pilgrim city.",
      category: "Spirituality",
      image: "https://images.unsplash.com/photo-1642740041801-cbe307fc400c?q=80&w=2035&auto=format&fit=crop",
      author: "Rajesh Patel",
      date: "April 5, 2025",
      readTime: "11 min read"
    },
    {
      id: 3,
      title: "Kumbh Mela 2027: Everything You Need to Know",
      excerpt: "Planning guide for the world's largest religious gathering coming to Nashik.",
      category: "Events",
      image: "https://images.unsplash.com/photo-1581337666064-8433d0109eee?q=80&w=1974&auto=format&fit=crop",
      author: "Priya Desai",
      date: "March 28, 2025",
      readTime: "15 min read"
    },
    {
      id: 4,
      title: "Hidden Gems: Off-the-Beaten-Path Attractions in Nashik",
      excerpt: "Discover lesser-known spots that showcase the authentic charm of Nashik.",
      category: "Adventure",
      image: "https://images.unsplash.com/photo-1590274853856-f22d5ee1c03f?q=80&w=2071&auto=format&fit=crop",
      author: "Amit Singh",
      date: "March 22, 2025",
      readTime: "9 min read"
    },
    {
      id: 5,
      title: "The Perfect Weekend Itinerary for Nashik",
      excerpt: "Make the most of your 2-day visit with this carefully curated travel plan.",
      category: "Travel Guide",
      image: "https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=2070&auto=format&fit=crop",
      author: "Meera Kapoor",
      date: "March 15, 2025",
      readTime: "7 min read"
    },
    {
      id: 6,
      title: "Seasonal Guide: When to Visit Nashik",
      excerpt: "Find the perfect time to visit based on weather, festivals, and vineyard activities.",
      category: "Travel Tips",
      image: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2070&auto=format&fit=crop",
      author: "Sanjay Mehta",
      date: "March 8, 2025",
      readTime: "6 min read"
    }
  ];

  const categories = [
    "Wine Tourism", 
    "Spirituality", 
    "Food & Dining", 
    "Adventure", 
    "Culture & History",
    "Events",
    "Travel Tips",
    "Accommodations"
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow container py-12">
        <div className="flex flex-col md:flex-row justify-between items-start gap-8">
          <div className="w-full md:w-2/3">
            <h1 className="text-4xl font-bold mb-2">Tourism Blog</h1>
            <p className="text-muted-foreground mb-8">Stories, guides and insights from Nashik</p>
            
            <Tabs defaultValue="all" className="mb-10">
              <TabsList className="mb-6 overflow-x-auto flex w-full md:w-auto">
                <TabsTrigger value="all">All Posts</TabsTrigger>
                <TabsTrigger value="wine">Wine Tourism</TabsTrigger>
                <TabsTrigger value="spiritual">Spirituality</TabsTrigger>
                <TabsTrigger value="guides">Travel Guides</TabsTrigger>
              </TabsList>
              
              <TabsContent value="all" className="mt-0">
                <div className="grid gap-8">
                  {/* Featured post */}
                  <Card className="overflow-hidden mb-6">
                    <div className="grid md:grid-cols-2">
                      <div className="h-64 md:h-full">
                        <img 
                          src={blogPosts[0].image}
                          alt={blogPosts[0].title}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className="p-6 flex flex-col justify-between">
                        <div>
                          <div className="inline-block bg-primary/10 text-primary text-xs font-medium px-2.5 py-1 rounded mb-3">
                            {blogPosts[0].category}
                          </div>
                          <h2 className="text-2xl font-bold mb-2">{blogPosts[0].title}</h2>
                          <p className="text-muted-foreground mb-4">{blogPosts[0].excerpt}</p>
                        </div>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center text-sm text-muted-foreground">
                            <User className="h-4 w-4 mr-1" />
                            <span>{blogPosts[0].author}</span>
                            <span className="mx-2">•</span>
                            <Clock className="h-4 w-4 mr-1" />
                            <span>{blogPosts[0].readTime}</span>
                          </div>
                          <Button variant="ghost" size="sm" className="flex items-center gap-1">
                            Read more <ArrowRight className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  </Card>
                  
                  {/* Regular posts */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {blogPosts.slice(1).map(post => (
                      <Card key={post.id} className="overflow-hidden card-hover">
                        <div className="h-48">
                          <img 
                            src={post.image}
                            alt={post.title}
                            className="w-full h-full object-cover transition-transform hover:scale-105 duration-300"
                          />
                        </div>
                        <CardHeader>
                          <div className="inline-block bg-primary/10 text-primary text-xs font-medium px-2.5 py-1 rounded mb-2">
                            {post.category}
                          </div>
                          <CardTitle className="text-lg">{post.title}</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <p className="text-muted-foreground">{post.excerpt}</p>
                        </CardContent>
                        <CardFooter className="flex items-center justify-between">
                          <div className="flex items-center text-xs text-muted-foreground">
                            <Calendar className="h-3 w-3 mr-1" />
                            <span>{post.date}</span>
                          </div>
                          <Button variant="ghost" size="sm" className="flex items-center gap-1">
                            Read more <ArrowRight className="h-3 w-3" />
                          </Button>
                        </CardFooter>
                      </Card>
                    ))}
                  </div>
                  
                  <div className="flex justify-center mt-8">
                    <Button variant="outline">Load More Articles</Button>
                  </div>
                </div>
              </TabsContent>
              
              <TabsContent value="wine" className="mt-0">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {blogPosts.filter(post => post.category === "Wine Tourism").map(post => (
                    <Card key={post.id} className="overflow-hidden card-hover">
                      <div className="h-48">
                        <img 
                          src={post.image}
                          alt={post.title}
                          className="w-full h-full object-cover transition-transform hover:scale-105 duration-300"
                        />
                      </div>
                      <CardHeader>
                        <div className="inline-block bg-primary/10 text-primary text-xs font-medium px-2.5 py-1 rounded mb-2">
                          {post.category}
                        </div>
                        <CardTitle className="text-lg">{post.title}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <p className="text-muted-foreground">{post.excerpt}</p>
                      </CardContent>
                      <CardFooter className="flex items-center justify-between">
                        <div className="flex items-center text-xs text-muted-foreground">
                          <Calendar className="h-3 w-3 mr-1" />
                          <span>{post.date}</span>
                        </div>
                        <Button variant="ghost" size="sm" className="flex items-center gap-1">
                          Read more <ArrowRight className="h-3 w-3" />
                        </Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              </TabsContent>
              
              <TabsContent value="spiritual" className="mt-0">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {blogPosts.filter(post => post.category === "Spirituality").map(post => (
                    <Card key={post.id} className="overflow-hidden card-hover">
                      <div className="h-48">
                        <img 
                          src={post.image}
                          alt={post.title}
                          className="w-full h-full object-cover transition-transform hover:scale-105 duration-300"
                        />
                      </div>
                      <CardHeader>
                        <div className="inline-block bg-primary/10 text-primary text-xs font-medium px-2.5 py-1 rounded mb-2">
                          {post.category}
                        </div>
                        <CardTitle className="text-lg">{post.title}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <p className="text-muted-foreground">{post.excerpt}</p>
                      </CardContent>
                      <CardFooter className="flex items-center justify-between">
                        <div className="flex items-center text-xs text-muted-foreground">
                          <Calendar className="h-3 w-3 mr-1" />
                          <span>{post.date}</span>
                        </div>
                        <Button variant="ghost" size="sm" className="flex items-center gap-1">
                          Read more <ArrowRight className="h-3 w-3" />
                        </Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              </TabsContent>
              
              <TabsContent value="guides" className="mt-0">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {blogPosts.filter(post => post.category === "Travel Guide" || post.category === "Travel Tips").map(post => (
                    <Card key={post.id} className="overflow-hidden card-hover">
                      <div className="h-48">
                        <img 
                          src={post.image}
                          alt={post.title}
                          className="w-full h-full object-cover transition-transform hover:scale-105 duration-300"
                        />
                      </div>
                      <CardHeader>
                        <div className="inline-block bg-primary/10 text-primary text-xs font-medium px-2.5 py-1 rounded mb-2">
                          {post.category}
                        </div>
                        <CardTitle className="text-lg">{post.title}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <p className="text-muted-foreground">{post.excerpt}</p>
                      </CardContent>
                      <CardFooter className="flex items-center justify-between">
                        <div className="flex items-center text-xs text-muted-foreground">
                          <Calendar className="h-3 w-3 mr-1" />
                          <span>{post.date}</span>
                        </div>
                        <Button variant="ghost" size="sm" className="flex items-center gap-1">
                          Read more <ArrowRight className="h-3 w-3" />
                        </Button>
                      </CardFooter>
                    </Card>
                  ))}
                </div>
              </TabsContent>
            </Tabs>
          </div>
          
          <div className="w-full md:w-1/3 space-y-8">
            <div className="bg-muted/50 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-4">Search Articles</h3>
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input type="search" placeholder="Search blog posts..." className="pl-9" />
              </div>
            </div>
            
            <div className="bg-muted/50 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-4">Categories</h3>
              <ul className="space-y-2">
                {categories.map(category => (
                  <li key={category}>
                    <Link to="#" className="flex items-center justify-between text-muted-foreground hover:text-foreground transition-colors">
                      <span>{category}</span>
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="bg-muted/50 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-4">Popular Posts</h3>
              <div className="space-y-4">
                {blogPosts.slice(0, 3).map(post => (
                  <div key={post.id} className="flex gap-4">
                    <div className="w-20 h-20 flex-shrink-0">
                      <img 
                        src={post.image} 
                        alt={post.title}
                        className="w-full h-full object-cover rounded-md"
                      />
                    </div>
                    <div>
                      <Link to="#" className="font-medium hover:text-primary transition-colors line-clamp-2">
                        {post.title}
                      </Link>
                      <p className="text-xs text-muted-foreground mt-1">{post.date}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="bg-primary/10 p-6 rounded-lg text-center">
              <h3 className="text-lg font-semibold mb-3">Subscribe to Our Newsletter</h3>
              <p className="text-sm text-muted-foreground mb-4">Get the latest updates on Nashik tourism delivered to your inbox</p>
              <Input placeholder="Your email address" className="mb-3" />
              <Button className="w-full">Subscribe</Button>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Blog;
