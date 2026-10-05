interface QuickSuggestionProps {
  suggestions: string[];
  onSelect: (suggestion: string) => void;
}

const QuickSuggestions = ({ suggestions, onSelect }: QuickSuggestionProps) => {
  return (
    <div className="flex flex-wrap gap-2">
      {suggestions.map((suggestion) => (
        <button
          key={suggestion}
          onClick={() => onSelect(suggestion)}
          className="px-4 py-2 rounded-full bg-secondary/80 hover:bg-secondary text-secondary-foreground text-sm font-medium transition-colors border border-border/50 hover:border-primary/30"
        >
          {suggestion}
        </button>
      ))}
    </div>
  );
};

export default QuickSuggestions;
