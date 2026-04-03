
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { HeroSection } from "@/components/home/HeroSection";
import { QuickLinksSection } from "@/components/home/QuickLinksSection";
import { KumbhMelaSection } from "@/components/home/KumbhMelaSection";
import { PopularAttractionsSection } from "@/components/home/PopularAttractionsSection";
import { NewsletterSection } from "@/components/home/NewsletterSection";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <HeroSection />
      <QuickLinksSection />
      <KumbhMelaSection />
      <PopularAttractionsSection />
      <NewsletterSection />
      <Footer />
    </div>
  );
};

export default Index;
