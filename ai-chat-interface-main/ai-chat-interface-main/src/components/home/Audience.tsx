import { Users, Plane, Camera, Briefcase } from "lucide-react";

const audiences = [
  {
    icon: Plane,
    title: "Voyageurs Indépendants",
    description: "Planifiez votre itinéraire idéal sans guide touristique",
  },
  {
    icon: Users,
    title: "Familles",
    description: "Trouvez des activités adaptées à tous les âges",
  },
  {
    icon: Camera,
    title: "Photographes",
    description: "Découvrez les spots les plus photogéniques",
  },
  {
    icon: Briefcase,
    title: "Voyages d'Affaires",
    description: "Optimisez votre temps libre entre réunions",
  },
];

const Audience = () => {
  return (
    <section className="py-20 bg-muted/30">
      <div className="container mx-auto px-4">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h2 className="font-heading text-3xl md:text-4xl font-bold mb-4">
            Pour qui ?
          </h2>
          <p className="text-muted-foreground text-lg">
            ExploreSmart s'adapte à tous les profils de voyageurs
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {audiences.map((audience, index) => (
            <div
              key={audience.title}
              className="text-center p-6 rounded-2xl bg-background border border-border hover:border-primary/30 transition-colors animate-slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="w-16 h-16 mx-auto rounded-full bg-primary/10 flex items-center justify-center mb-4">
                <audience.icon className="w-8 h-8 text-primary" />
              </div>
              <h3 className="font-heading font-semibold text-lg mb-2">
                {audience.title}
              </h3>
              <p className="text-sm text-muted-foreground">
                {audience.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Audience;
