export function accessStatusLabel(status: string | null | undefined): string {
  switch (status) {
    case "OPEN_ACCESS":
      return "Open access";
    case "ABSTRACT_ONLY":
      return "Only abstract";
    case "INSTITUTIONAL_ACCESS_NEEDED":
      return "Institutional access";
    case "UNKNOWN":
    default:
      return "Full text unknown";
  }
}

export function accessStatusHelp(status: string | null | undefined): string {
  switch (status) {
    case "OPEN_ACCESS":
      return "Unpaywall or source metadata indicates that a public full text is available.";
    case "ABSTRACT_ONLY":
      return "The system found an abstract, but no public full-text access label.";
    case "INSTITUTIONAL_ACCESS_NEEDED":
      return "The article may require institutional or paid access.";
    case "UNKNOWN":
    default:
      return "Access metadata was incomplete, often because DOI or Unpaywall data was unavailable.";
  }
}

export function recommendationLabel(level: string | null | undefined): string {
  switch (level) {
    case "must_read":
      return "Must read";
    case "high":
      return "High priority";
    case "medium":
      return "Medium priority";
    case "low":
      return "Low priority";
    case "important":
      return "Important";
    default:
      return level ?? "Unrated";
  }
}
