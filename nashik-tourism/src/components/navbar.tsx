
import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { ThemeToggle } from "./theme-toggle";
import { Button } from "@/components/ui/button";
import { NavigationMenu, NavigationMenuContent, NavigationMenuItem, NavigationMenuLink, NavigationMenuList, NavigationMenuTrigger } from "@/components/ui/navigation-menu";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { cn } from "@/lib/utils";
import { Menu, X, ChevronDown, ChevronRight, Globe } from "lucide-react";
import { useTheme } from "./theme-provider";
import { useIsMobile } from "@/hooks/use-mobile";
import { 
  DropdownMenu, 
  DropdownMenuTrigger, 
  DropdownMenuContent, 
  DropdownMenuItem,
  DropdownMenuSeparator 
} from "@/components/ui/dropdown-menu";

const mainNav = [{
  title: "Home",
  href: "/"
}, {
  title: "Kumbh Mela 2027",
  href: "/kumbh-mela"
}, {
  title: "Discover Nashik",
  href: "/discover",
  submenus: [{
    title: "Sula Vineyards",
    href: "/discover/sula-vineyards"
  }, {
    title: "Trimbakeshwar Temple",
    href: "/discover/trimbakeshwar"
  }, {
    title: "Pandavleni Caves",
    href: "/discover/pandavleni"
  }, {
    title: "All Destinations",
    href: "/discover"
  }]
}, {
  title: "Plan My Trip",
  href: "/plan-trip"
}, {
  title: "Book Hotels",
  href: "/hotels"
}, {
  title: "Blog",
  href: "/blog"
}, {
  title: "Contact",
  href: "/contact"
}];

const languages = [{
  label: "English",
  value: "en"
}, {
  label: "हिंदी",
  value: "hi"
}, {
  label: "मराठी",
  value: "mr"
}];

export function Navbar() {
  const [currentLanguage, setCurrentLanguage] = useState(languages[0]);
  const { theme } = useTheme();
  const [isScrolled, setIsScrolled] = useState(false);
  const isMobile = useIsMobile();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  // Detect scroll to add shadow/background opacity changes
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);
  
  // Close mobile menu on route change
  useEffect(() => {
    setIsMenuOpen(false);
  }, [location.pathname]);
  
  // Check if route is active
  const isActiveRoute = (path: string) => {
    if (path === '/') {
      return location.pathname === path;
    }
    return location.pathname.startsWith(path);
  };

  return (
    <header 
      className={cn(
        "sticky top-0 z-50 w-full transition-all duration-300",
        "dark:bg-[rgba(30,30,30,0.5)] bg-[rgba(255,255,255,0.6)]",
        "backdrop-blur-md border-b dark:border-white/10 border-black/5",
        "shadow-sm dark:shadow-[0_4px_12px_-2px_rgba(0,0,0,0.3)] shadow-[0_4px_12px_-2px_rgba(0,0,0,0.1)]",
        isScrolled && "dark:bg-[rgba(30,30,30,0.8)] bg-[rgba(255,255,255,0.9)] shadow-md"
      )}
    >
      <div className="container flex h-16 items-center justify-between px-4 sm:px-6">
        <Link to="/" className="flex items-center">
          <img 
            src={theme === 'dark' 
              ? "/lovable-uploads/6d2af758-5f3c-4a05-b62e-83a9ddcc49c6.png"
              : "/lovable-uploads/fefe6db1-4efb-4f4e-9f66-cdcb87409882.png"} 
            alt="Nashik Tourism Logo" 
            className="h-12 w-12 sm:h-16 sm:w-16 md:h-20 md:w-20 object-contain transition-transform duration-300 hover:scale-105" 
          />
        </Link>
        
        {!isMobile ? (
          <nav className="flex items-center gap-6">
            <NavigationMenu className="transition-colors">
              <NavigationMenuList>
                {mainNav.map(item => 
                  item.submenus ? (
                    <NavigationMenuItem key={item.title}>
                      <NavigationMenuTrigger 
                        className={cn(
                          "dark:hover:bg-white/10 hover:bg-black/5 transition-colors",
                          isActiveRoute(item.href) && "text-primary font-medium"
                        )}
                      >
                        {item.title}
                      </NavigationMenuTrigger>
                      <NavigationMenuContent>
                        <ul className="grid w-[400px] gap-3 p-4 dark:bg-[rgba(30,30,30,0.9)] bg-[rgba(255,255,255,0.9)] backdrop-blur-md rounded-xl">
                          {item.submenus.map(submenu => (
                            <li key={submenu.title}>
                              <NavigationMenuLink asChild>
                                <Link 
                                  to={submenu.href} 
                                  className={cn(
                                    "block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors",
                                    "hover:bg-black/5 dark:hover:bg-white/10",
                                    "focus:bg-black/5 dark:focus:bg-white/10",
                                    isActiveRoute(submenu.href) && "bg-black/5 dark:bg-white/10"
                                  )}
                                >
                                  <div className={cn(
                                    "text-sm font-medium leading-none",
                                    isActiveRoute(submenu.href) && "text-primary"
                                  )}>
                                    {submenu.title}
                                  </div>
                                </Link>
                              </NavigationMenuLink>
                            </li>
                          ))}
                        </ul>
                      </NavigationMenuContent>
                    </NavigationMenuItem>
                  ) : (
                    <NavigationMenuItem key={item.title}>
                      <Link 
                        to={item.href} 
                        className={cn(
                          "group inline-flex h-10 w-max items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors",
                          "hover:bg-black/5 dark:hover:bg-white/10 focus:bg-black/5 dark:focus:bg-white/10",
                          isActiveRoute(item.href) && "text-primary font-medium"
                        )}
                      >
                        {item.title}
                      </Link>
                    </NavigationMenuItem>
                  )
                )}
              </NavigationMenuList>
            </NavigationMenu>
            
            <div className="flex items-center gap-4">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button 
                    variant="ghost" 
                    size="sm"
                    className="flex items-center gap-2 hover:bg-black/5 dark:hover:bg-white/10"
                  >
                    <Globe className="h-4 w-4" />
                    <span>{currentLanguage.label}</span>
                    <ChevronDown className="h-3 w-3 opacity-50" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-40 dark:bg-[rgba(30,30,30,0.9)] bg-[rgba(255,255,255,0.9)] backdrop-blur-md">
                  {languages.map((lang) => (
                    <DropdownMenuItem
                      key={lang.value}
                      className={cn(
                        "cursor-pointer",
                        currentLanguage.value === lang.value ? "bg-black/5 dark:bg-white/10 font-medium" : ""
                      )}
                      onClick={() => setCurrentLanguage(lang)}
                    >
                      {lang.label}
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
              <ThemeToggle />
            </div>
          </nav>
        ) : (
          <div className="flex items-center gap-4">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className="rounded-full hover:bg-black/5 dark:hover:bg-white/10"
                >
                  <Globe className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-40 dark:bg-[rgba(30,30,30,0.9)] bg-[rgba(255,255,255,0.9)] backdrop-blur-md">
                {languages.map((lang) => (
                  <DropdownMenuItem
                    key={lang.value}
                    className={cn(
                      "cursor-pointer",
                      currentLanguage.value === lang.value ? "bg-black/5 dark:bg-white/10 font-medium" : ""
                    )}
                    onClick={() => setCurrentLanguage(lang)}
                  >
                    {lang.label}
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          
            <ThemeToggle />
            
            <Sheet open={isMenuOpen} onOpenChange={setIsMenuOpen}>
              <SheetTrigger asChild>
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className="rounded-full hover:bg-black/5 dark:hover:bg-white/10"
                  aria-label="Open mobile menu"
                >
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-[85%] max-w-[400px] p-0">
                <SheetHeader className="p-6 border-b">
                  <SheetTitle className="flex items-center justify-start">
                    <img 
                      src={theme === 'dark' 
                        ? "/lovable-uploads/6d2af758-5f3c-4a05-b62e-83a9ddcc49c6.png"
                        : "/lovable-uploads/fefe6db1-4efb-4f4e-9f66-cdcb87409882.png"} 
                      alt="Nashik Tourism Logo" 
                      className="h-12 w-12 object-contain mr-3" 
                    />
                    Nashik Tourism
                  </SheetTitle>
                </SheetHeader>
                
                <div className="py-6 px-4 flex flex-col gap-1 overflow-y-auto max-h-[calc(100vh-80px)]">
                  {mainNav.map(item => (
                    <div key={item.title} className="mb-2">
                      {item.submenus ? (
                        <details className="group">
                          <summary className="list-none flex items-center justify-between cursor-pointer py-3 px-3 rounded-md hover:bg-black/5 dark:hover:bg-white/10 min-h-[48px]">
                            <span className={cn(
                              "font-medium",
                              isActiveRoute(item.href) && "text-primary"
                            )}>
                              {item.title}
                            </span>
                            <ChevronDown className="h-4 w-4 transition-transform group-open:rotate-180" />
                          </summary>
                          <div className="pl-4 mt-1 space-y-1">
                            {item.submenus.map(submenu => (
                              <Link 
                                key={submenu.title} 
                                to={submenu.href} 
                                className={cn(
                                  "block py-3 px-3 rounded-md text-sm hover:bg-black/5 dark:hover:bg-white/10 min-h-[48px] flex items-center",
                                  isActiveRoute(submenu.href) && "text-primary font-medium bg-black/5 dark:bg-white/5"
                                )}
                              >
                                <div className="flex items-center">
                                  <ChevronRight className="h-3 w-3 mr-2 flex-shrink-0" />
                                  {submenu.title}
                                </div>
                              </Link>
                            ))}
                          </div>
                        </details>
                      ) : (
                        <Link 
                          to={item.href} 
                          className={cn(
                            "block py-3 px-3 rounded-md hover:bg-black/5 dark:hover:bg-white/10 min-h-[48px] flex items-center",
                            isActiveRoute(item.href) && "text-primary font-medium bg-black/5 dark:bg-white/5"
                          )}
                        >
                          {item.title}
                        </Link>
                      )}
                    </div>
                  ))}
                </div>
                
                <div className="mt-auto border-t p-6">
                  <div className="flex flex-col gap-2">
                    <div className="text-sm text-muted-foreground mb-2">Language</div>
                    {languages.map(lang => (
                      <Button 
                        key={lang.value} 
                        variant="ghost" 
                        onClick={() => setCurrentLanguage(lang)} 
                        className={cn(
                          "justify-start text-sm hover:bg-black/5 dark:hover:bg-white/10",
                          currentLanguage.value === lang.value ? "bg-black/5 dark:bg-white/10 font-medium" : ""
                        )}
                      >
                        {lang.label}
                      </Button>
                    ))}
                  </div>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        )}
      </div>
    </header>
  );
}
