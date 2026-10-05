import { Bot, MapPin, Zap, Heart, Globe, Shield } from "lucide-react";

const features = [
  {
    icon: Bot,
    title: "Assistant IA Intelligent",
    description: "Discutez naturellement avec notre chatbot qui comprend vos préférences et besoins de voyage.",
    color: "bg-primary/10 text-primary",
  },
  {
    icon: MapPin,
    title: "Recommandations Personnalisées",
    description: "Obtenez des suggestions de lieux adaptées à vos envies : plage, culture, aventure ou détente.",
    color: "bg-accent/10 text-accent",
  },
  {
    icon: Zap,
    title: "Réponses Instantanées",
    description: "Notre système analyse votre demande en temps réel pour des recommandations immédiates.",
    color: "bg-sunset/10 text-sunset",
  },
  {
    icon: Heart,
    title: "Expériences Uniques",
    description: "Découvrez des destinations hors des sentiers battus sélectionnées par notre IA.",
    color: "bg-destructive/10 text-destructive",
  },
  {
    icon: Globe,
    title: "Couverture Complète",
    description: "Des plages d'Agadir aux dunes de Merzouga, explorez tout le Maroc.",
    color: "bg-ocean/10 text-ocean",
  },
  {
    icon: Shield,
    title: "Informations Fiables",
    description: "Données vérifiées avec coordonnées GPS et liens Google Maps directs.",
    color: "bg-nature/10 text-nature",
  },
];

const Features = () => {
  return (
    <section id="features" className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="font-heading text-3xl md:text-4xl font-bold mb-4">
            Pourquoi choisir{" "}
            <span className="gradient-text">ExploreSmart</span> ?
          </h2>
          <p className="text-muted-foreground text-lg">
            Une technologie de pointe au service de votre exploration
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className="card-travel p-6 md:p-8 animate-fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div
                className={`w-14 h-14 rounded-2xl ${feature.color} flex items-center justify-center mb-5`}
              >
                <feature.icon className="w-7 h-7" />
              </div>
              <h3 className="font-heading font-semibold text-xl mb-3">
                {feature.title}
              </h3>
              <p className="text-muted-foreground leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
