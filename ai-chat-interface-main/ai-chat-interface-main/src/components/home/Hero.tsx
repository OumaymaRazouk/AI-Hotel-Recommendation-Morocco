import { Link } from "react-router-dom";
import { Sparkles, MapPin, ArrowRight, Palmtree, Sun, Waves } from "lucide-react";

const Hero = () => {
  return (
    <section className="relative min-h-screen hero-bg overflow-hidden pt-16">
      {/* Decorative Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 text-primary/20 animate-float">
          <Palmtree className="w-16 h-16 md:w-24 md:h-24" />
        </div>
        <div className="absolute top-40 right-10 text-sunset/30 animate-bounce-soft">
          <Sun className="w-12 h-12 md:w-20 md:h-20" />
        </div>
        <div className="absolute bottom-40 left-20 text-primary/15 animate-float stagger-2">
          <Waves className="w-20 h-20 md:w-32 md:h-32" />
        </div>
        {/* Gradient Orbs */}
        <div className="absolute top-1/4 -right-20 w-96 h-96 bg-primary/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 -left-20 w-80 h-80 bg-sunset/10 rounded-full blur-3xl" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] text-center py-12">
          {/* Badge */}
          <div className="animate-fade-in inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">
              Recommandations IA pour touristes
            </span>
          </div>

          {/* Main Title */}
          <h1 className="animate-slide-up font-heading text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold mb-6 max-w-4xl">
            Découvrez les{" "}
            <span className="gradient-text">merveilles</span>
            {" "}du Maroc
          </h1>

          {/* Subtitle */}
          <p className="animate-slide-up stagger-1 text-lg md:text-xl text-muted-foreground max-w-2xl mb-8">
            Notre assistant intelligent vous guide vers les destinations 
            parfaites selon vos envies. Plages, déserts, médinas ou montagnes — 
            trouvez votre prochaine aventure.
          </p>

          {/* CTA Buttons */}
          <div className="animate-slide-up stagger-2 flex flex-col sm:flex-row gap-4">
            <Link
              to="/chatbot"
              className="btn-primary inline-flex items-center justify-center gap-2 px-8 py-4 rounded-full text-lg font-semibold text-primary-foreground"
            >
              <MapPin className="w-5 h-5" />
              Explorer maintenant
              <ArrowRight className="w-5 h-5" />
            </Link>
            <a
              href="#features"
              className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-full text-lg font-semibold border-2 border-border hover:bg-muted transition-colors"
            >
              En savoir plus
            </a>
          </div>

          {/* Stats */}
          <div className="animate-slide-up stagger-3 mt-16 grid grid-cols-3 gap-8 md:gap-16">
            {[
              { value: "10+", label: "Destinations" },
              { value: "24/7", label: "Disponibilité" },
              { value: "100%", label: "Gratuit" },
            ].map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-3xl md:text-4xl font-heading font-bold gradient-text">
                  {stat.value}
                </div>
                <div className="text-sm text-muted-foreground mt-1">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Wave Decoration */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg
          viewBox="0 0 1440 120"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-full"
        >
          <path
            d="M0 120L60 110C120 100 240 80 360 70C480 60 600 60 720 65C840 70 960 80 1080 85C1200 90 1320 90 1380 90L1440 90V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z"
            fill="hsl(var(--background))"
          />
        </svg>
      </div>
    </section>
  );
};

export default Hero;
