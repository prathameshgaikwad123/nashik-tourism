
import { Link } from "react-router-dom";
import { Facebook, Instagram, Twitter, Youtube, MapPin, Phone, Mail } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-background border-t">
      <div className="container py-10 md:py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">Nashik Tourism</h3>
            <p className="text-muted-foreground mb-4">
              Explore the divine city of Nashik, home to ancient temples, world-class wineries, and the sacred Kumbh Mela.
            </p>
            <div className="flex space-x-4">
              <a href="#" aria-label="Facebook" className="text-muted-foreground hover:text-primary transition-colors">
                <Facebook size={20} />
              </a>
              <a href="#" aria-label="Twitter" className="text-muted-foreground hover:text-primary transition-colors">
                <Twitter size={20} />
              </a>
              <a href="#" aria-label="Instagram" className="text-muted-foreground hover:text-primary transition-colors">
                <Instagram size={20} />
              </a>
              <a href="#" aria-label="YouTube" className="text-muted-foreground hover:text-primary transition-colors">
                <Youtube size={20} />
              </a>
            </div>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/kumbh-mela" className="text-muted-foreground hover:text-primary transition-colors">
                  Kumbh Mela 2027
                </Link>
              </li>
              <li>
                <Link to="/discover" className="text-muted-foreground hover:text-primary transition-colors">
                  Discover Nashik
                </Link>
              </li>
              <li>
                <Link to="/plan-trip" className="text-muted-foreground hover:text-primary transition-colors">
                  Plan My Trip
                </Link>
              </li>
              <li>
                <Link to="/hotels" className="text-muted-foreground hover:text-primary transition-colors">
                  Book Hotels
                </Link>
              </li>
              <li>
                <Link to="/blog" className="text-muted-foreground hover:text-primary transition-colors">
                  Blog
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Popular Attractions</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/discover/sula-vineyards" className="text-muted-foreground hover:text-primary transition-colors">
                  Sula Vineyards
                </Link>
              </li>
              <li>
                <Link to="/discover/trimbakeshwar" className="text-muted-foreground hover:text-primary transition-colors">
                  Trimbakeshwar Temple
                </Link>
              </li>
              <li>
                <Link to="/discover/pandavleni" className="text-muted-foreground hover:text-primary transition-colors">
                  Pandavleni Caves
                </Link>
              </li>
              <li>
                <Link to="/discover" className="text-muted-foreground hover:text-primary transition-colors">
                  View All Attractions
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Contact Us</h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-2">
                <MapPin size={20} className="text-primary mt-1 flex-shrink-0" />
                <span className="text-muted-foreground">
                  Tourism Information Center, Nashik, Maharashtra, India
                </span>
              </li>
              <li className="flex items-center gap-2">
                <Phone size={18} className="text-primary flex-shrink-0" />
                <span className="text-muted-foreground">+91 1234567890</span>
              </li>
              <li className="flex items-center gap-2">
                <Mail size={18} className="text-primary flex-shrink-0" />
                <span className="text-muted-foreground">info@nashiktourism.com</span>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t mt-10 pt-6 flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm text-muted-foreground mb-4 md:mb-0">
            &copy; {new Date().getFullYear()} Nashik Tourism. All rights reserved.
          </p>
          <div className="flex space-x-6">
            <Link to="/privacy-policy" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              Privacy Policy
            </Link>
            <Link to="/terms" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              Terms of Service
            </Link>
            <Link to="/sitemap" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              Sitemap
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
