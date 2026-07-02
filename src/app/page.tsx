import Header from "@/components/Header";
import Hero from "@/components/Hero";
import Positioning from "@/components/Positioning";
import ServicePillars from "@/components/ServicePillars";
import WhyUs from "@/components/WhyUs";
import WorkingMethod from "@/components/WorkingMethod";
import ContactSection from "@/components/ContactSection";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <>
      <Header />
      <main className="flex flex-1 flex-col">
        <Hero />
        <Positioning />
        <ServicePillars />
        <WhyUs />
        <WorkingMethod />
        <ContactSection />
      </main>
      <Footer />
    </>
  );
}
