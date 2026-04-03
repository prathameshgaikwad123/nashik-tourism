
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "@/components/theme-provider";

import Index from "./pages/Index";
import KumbhMela from "./pages/KumbhMela";
import Discover from "./pages/Discover";
import PlanTrip from "./pages/PlanTrip";
import Hotels from "./pages/Hotels";
import Blog from "./pages/Blog";
import Contact from "./pages/Contact";
import NotFound from "./pages/NotFound";
import SulaVineyards from "./pages/destinations/SulaVineyards";
import Trimbakeshwar from "./pages/destinations/Trimbakeshwar";
import Pandavleni from "./pages/destinations/Pandavleni";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider defaultTheme="light">
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/kumbh-mela" element={<KumbhMela />} />
            <Route path="/discover" element={<Discover />} />
            <Route path="/plan-trip" element={<PlanTrip />} />
            <Route path="/hotels" element={<Hotels />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/discover/sula-vineyards" element={<SulaVineyards />} />
            <Route path="/discover/trimbakeshwar" element={<Trimbakeshwar />} />
            <Route path="/discover/pandavleni" element={<Pandavleni />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </ThemeProvider>
  </QueryClientProvider>
);

export default App;
