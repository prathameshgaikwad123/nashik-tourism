
import { useState } from "react";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { MapPin, Mail, Phone, CheckCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const Contact = () => {
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { toast } = useToast();
  
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate form submission
    setTimeout(() => {
      setFormSubmitted(true);
      setIsSubmitting(false);
      toast({
        title: "Message Sent!",
        description: "We will contact you soon. Thank you for reaching out.",
      });
    }, 1000);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        {/* Hero Section */}
        <section className="relative h-[40vh] md:h-[50vh]">
          <img 
            src="https://images.unsplash.com/photo-1464746133101-a2c3f88e0dd9?q=80&w=2073&auto=format&fit=crop"
            alt="Nashik cityscape with vineyards and hills" 
            className="w-full h-full object-cover" 
          />
          <div className="absolute inset-0 bg-black/40 flex items-center">
            <div className="container">
              <h1 className="text-3xl md:text-5xl font-bold text-white mb-4">Contact Us</h1>
              <p className="text-lg text-white/90 max-w-2xl">
                Get in touch with our team for any questions about visiting Nashik
              </p>
            </div>
          </div>
        </section>

        <div className="container py-12">
          <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-8 lg:gap-12">
            <div>
              <h2 className="text-2xl font-bold mb-6">We're Here to Help</h2>
              <p className="text-muted-foreground mb-8">
                Planning a trip to Nashik? Have questions about attractions, accommodations, 
                or local experiences? Our tourism experts are ready to assist you and make your 
                visit to Nashik unforgettable.
              </p>
              
              <div className="space-y-6">
                <div className="flex items-start gap-4">
                  <div className="bg-primary/10 p-2.5 rounded-full">
                    <MapPin className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold mb-1">Address</h3>
                    <p className="text-muted-foreground">
                      Tourism Information Center<br />
                      Nashik, Maharashtra<br />
                      India - 422001
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start gap-4">
                  <div className="bg-primary/10 p-2.5 rounded-full">
                    <Mail className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold mb-1">Email</h3>
                    <p className="text-muted-foreground">info@nashiktourism.com</p>
                    <p className="text-muted-foreground">support@nashiktourism.com</p>
                  </div>
                </div>
                
                <div className="flex items-start gap-4">
                  <div className="bg-primary/10 p-2.5 rounded-full">
                    <Phone className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold mb-1">Phone</h3>
                    <p className="text-muted-foreground">+91 253 2590750</p>
                    <p className="text-muted-foreground">+91 8888776655 (Tourism Helpline)</p>
                  </div>
                </div>
              </div>
              
              <div className="mt-8 bg-muted/50 p-6 rounded-lg">
                <h3 className="font-semibold mb-3">Tourism Office Hours</h3>
                <ul className="space-y-2 text-muted-foreground">
                  <li className="flex justify-between">
                    <span>Monday - Friday:</span>
                    <span>9:00 AM - 6:00 PM</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Saturday:</span>
                    <span>10:00 AM - 4:00 PM</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Sunday:</span>
                    <span>Closed</span>
                  </li>
                </ul>
              </div>
            </div>
            
            <div className="bg-card rounded-lg p-6 shadow-sm border">
              {formSubmitted ? (
                <div className="h-full flex flex-col items-center justify-center text-center py-8">
                  <div className="bg-primary/10 p-3 rounded-full mb-4">
                    <CheckCircle className="w-8 h-8 text-primary" />
                  </div>
                  <h2 className="text-2xl font-semibold mb-3">Message Received!</h2>
                  <p className="text-muted-foreground mb-6 max-w-md">
                    Thank you for contacting Nashik Tourism. Our team will review your message and get back to you within 24-48 hours.
                  </p>
                  <Button onClick={() => setFormSubmitted(false)}>Send Another Message</Button>
                </div>
              ) : (
                <>
                  <h2 className="text-2xl font-semibold mb-6">Send us a Message</h2>
                  <form className="space-y-4" onSubmit={handleSubmit}>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="name" className="block text-sm font-medium mb-1">Your Name</label>
                        <Input id="name" placeholder="Full name" required />
                      </div>
                      <div>
                        <label htmlFor="email" className="block text-sm font-medium mb-1">Email Address</label>
                        <Input id="email" type="email" placeholder="youremail@example.com" required />
                      </div>
                    </div>
                    <div>
                      <label htmlFor="subject" className="block text-sm font-medium mb-1">Subject</label>
                      <Input id="subject" placeholder="How can we help?" required />
                    </div>
                    <div>
                      <label htmlFor="message" className="block text-sm font-medium mb-1">Your Message</label>
                      <Textarea 
                        id="message" 
                        placeholder="Write your message here..." 
                        className="min-h-[120px]" 
                        required
                      />
                    </div>
                    <div className="mt-2">
                      <Button 
                        type="submit" 
                        className="w-full" 
                        disabled={isSubmitting}
                      >
                        {isSubmitting ? "Sending..." : "Send Message"}
                      </Button>
                    </div>
                  </form>
                </>
              )}
            </div>
          </div>
        </div>
        
        {/* Map Section */}
        <div className="h-[400px] mt-10">
          <iframe 
            title="Nashik Map"
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d120128.29041731564!2d73.71459543392329!3d19.987328747684196!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bddeaaa7d92580d%3A0xbad9ed0e30aedf75!2sNashik%2C%20Maharashtra!5e0!3m2!1sen!2sin!4v1712838293834!5m2!1sen!2sin" 
            width="100%" 
            height="100%" 
            style={{ border: 0 }} 
            allowFullScreen={false} 
            loading="lazy" 
            referrerPolicy="no-referrer-when-downgrade"
            className="block w-full"
          />
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Contact;
