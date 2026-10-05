export interface Place {
  id: number;
  name: string;
  city: string;
  description: string;
  latitude: number;
  longitude: number;
  tags: string[];
  image: string;
  rating: number;
}

export const places: Place[] = [
  {
    id: 1,
    name: "Plage d'Agadir",
    city: "Agadir",
    description: "Magnifique plage de sable fin s'étendant sur 10 km, idéale pour la baignade et les sports nautiques. Coucher de soleil spectaculaire.",
    latitude: 30.4278,
    longitude: -9.5981,
    tags: ["plage", "mer", "soleil", "sports nautiques", "détente"],
    image: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
    rating: 4.7,
  },
  {
    id: 2,
    name: "Médina de Marrakech",
    city: "Marrakech",
    description: "Cœur historique de Marrakech avec ses souks colorés, ses palais et la célèbre place Jemaa el-Fna. Patrimoine UNESCO.",
    latitude: 31.6295,
    longitude: -7.9811,
    tags: ["culture", "histoire", "shopping", "architecture", "souks"],
    image: "https://images.unsplash.com/photo-1539020140153-e479b8c22e70?w=800",
    rating: 4.8,
  },
  {
    id: 3,
    name: "Cascades d'Ouzoud",
    city: "Azilal",
    description: "Chutes d'eau de 110m de hauteur entourées d'oliviers. Observation des singes magots et randonnées dans un cadre naturel exceptionnel.",
    latitude: 32.0156,
    longitude: -6.7167,
    tags: ["nature", "cascade", "randonnée", "animaux", "photographie"],
    image: "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=800",
    rating: 4.6,
  },
  {
    id: 4,
    name: "Désert de Merzouga",
    city: "Merzouga",
    description: "Dunes dorées de l'Erg Chebbi, excursions en dromadaire, nuits sous les étoiles dans des camps berbères traditionnels.",
    latitude: 31.0801,
    longitude: -4.0133,
    tags: ["désert", "aventure", "dromadaire", "étoiles", "berbère"],
    image: "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=800",
    rating: 4.9,
  },
  {
    id: 5,
    name: "Chefchaouen",
    city: "Chefchaouen",
    description: "La perle bleue du Maroc. Ville pittoresque aux ruelles peintes en bleu, nichée dans les montagnes du Rif.",
    latitude: 35.1688,
    longitude: -5.2636,
    tags: ["ville bleue", "montagne", "photographie", "artisanat", "tranquillité"],
    image: "https://images.unsplash.com/photo-1553522991-71c5c1e38c68?w=800",
    rating: 4.8,
  },
  {
    id: 6,
    name: "Jardins Majorelle",
    city: "Marrakech",
    description: "Jardin botanique enchanteur créé par Jacques Majorelle, célèbre pour son bleu intense et sa collection de cactus.",
    latitude: 31.6417,
    longitude: -8.0033,
    tags: ["jardin", "art", "nature", "Yves Saint Laurent", "botanique"],
    image: "https://images.unsplash.com/photo-1570099029629-df5b7c6ceecf?w=800",
    rating: 4.5,
  },
  {
    id: 7,
    name: "Essaouira",
    city: "Essaouira",
    description: "Cité portuaire fortifiée, paradis des surfeurs et kitesurfeurs. Médina blanche et bleue, ambiance artistique unique.",
    latitude: 31.5085,
    longitude: -9.7595,
    tags: ["port", "surf", "art", "médina", "vent"],
    image: "https://images.unsplash.com/photo-1569383746724-6f1b882b8f46?w=800",
    rating: 4.7,
  },
  {
    id: 8,
    name: "Vallée du Dadès",
    city: "Boumalne Dadès",
    description: "Gorges spectaculaires et kasbahs en terre rouge. Route des mille kasbahs avec des paysages à couper le souffle.",
    latitude: 31.4833,
    longitude: -5.9833,
    tags: ["gorges", "kasbah", "paysage", "route", "montagne"],
    image: "https://images.unsplash.com/photo-1489749798305-4fea3ae63d43?w=800",
    rating: 4.6,
  },
  {
    id: 9,
    name: "Fès el-Bali",
    city: "Fès",
    description: "La plus grande médina médiévale du monde. Tanneries traditionnelles, mosquées anciennes et université millénaire.",
    latitude: 34.0619,
    longitude: -4.9731,
    tags: ["médina", "histoire", "tannerie", "artisanat", "UNESCO"],
    image: "https://images.unsplash.com/photo-1548017653-4e0f52d9f919?w=800",
    rating: 4.7,
  },
  {
    id: 10,
    name: "Baie de Dakhla",
    city: "Dakhla",
    description: "Lagune préservée entre océan et désert. Spot mondial de kitesurf et windsurf, faune marine exceptionnelle.",
    latitude: 23.7147,
    longitude: -15.9473,
    tags: ["lagune", "kitesurf", "désert", "nature", "aventure"],
    image: "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800",
    rating: 4.8,
  },
];

export const getGoogleMapsUrl = (place: Place): string => {
  return `https://www.google.com/maps?q=${place.latitude},${place.longitude}`;
};

export const searchPlaces = (query: string, topK: number = 5): Place[] => {
  const queryLower = query.toLowerCase();
  const queryWords = queryLower.split(/\s+/);

  const scoredPlaces = places.map((place) => {
    let score = 0;
    const searchText = `${place.name} ${place.city} ${place.description} ${place.tags.join(" ")}`.toLowerCase();

    queryWords.forEach((word) => {
      if (searchText.includes(word)) {
        score += 1;
        // Bonus for exact tag match
        if (place.tags.some((tag) => tag.toLowerCase().includes(word))) {
          score += 2;
        }
        // Bonus for city match
        if (place.city.toLowerCase().includes(word)) {
          score += 3;
        }
        // Bonus for name match
        if (place.name.toLowerCase().includes(word)) {
          score += 2;
        }
      }
    });

    return { place, score };
  });

  return scoredPlaces
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, topK)
    .map((item) => item.place);
};
