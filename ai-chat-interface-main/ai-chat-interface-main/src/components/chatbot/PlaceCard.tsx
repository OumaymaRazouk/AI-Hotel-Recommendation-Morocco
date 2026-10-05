import { MapPin, Star, ExternalLink } from "lucide-react";
import { Place, getGoogleMapsUrl } from "@/data/places";

interface PlaceCardProps {
  place: Place;
  index?: number;
}

const PlaceCard = ({ place, index = 0 }: PlaceCardProps) => {
  return (
    <div 
      className="place-card animate-slide-up"
      style={{ animationDelay: `${index * 0.1}s` }}
    >
      {/* Image */}
      <div className="relative h-40 overflow-hidden">
        <img
          src={place.image}
          alt={place.name}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        
        {/* Rating Badge */}
        <div className="absolute top-3 right-3 flex items-center gap-1 px-2 py-1 rounded-full bg-white/90 backdrop-blur-sm text-sm font-medium">
          <Star className="w-3.5 h-3.5 text-sunset fill-sunset" />
          <span>{place.rating}</span>
        </div>

        {/* City Badge */}
        <div className="absolute bottom-3 left-3 flex items-center gap-1 px-2 py-1 rounded-full bg-primary/90 text-white text-xs font-medium">
          <MapPin className="w-3 h-3" />
          {place.city}
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="font-heading font-semibold text-lg mb-2 line-clamp-1">
          {place.name}
        </h3>
        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {place.description}
        </p>

        {/* Tags */}
        <div className="flex flex-wrap gap-1.5 mb-4">
          {place.tags.slice(0, 3).map((tag) => (
            <span
              key={tag}
              className="px-2 py-0.5 rounded-full bg-muted text-xs text-muted-foreground"
            >
              {tag}
            </span>
          ))}
        </div>

        {/* Action */}
        <a
          href={getGoogleMapsUrl(place)}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 w-full justify-center px-4 py-2.5 rounded-xl bg-primary/10 text-primary hover:bg-primary/20 transition-colors text-sm font-medium"
        >
          <MapPin className="w-4 h-4" />
          Voir sur Google Maps
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      </div>
    </div>
  );
};

export default PlaceCard;
