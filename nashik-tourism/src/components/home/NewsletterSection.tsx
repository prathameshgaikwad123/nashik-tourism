
import { Button } from "@/components/ui/button";

export function NewsletterSection() {
  return (
    <section className="py-16 container">
      <div className="bg-primary/5 rounded-lg p-8 md:p-12">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">Stay Updated</h2>
          <p className="text-lg mb-6">Subscribe to our newsletter for the latest events, travel tips, and updates about Kumbh Mela 2027.</p>
          <form className="flex flex-col sm:flex-row gap-2">
            <input type="email" placeholder="Enter your email" className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50" />
            <Button type="submit" className="sm:w-auto">Subscribe</Button>
          </form>
        </div>
      </div>
    </section>
  );
}
