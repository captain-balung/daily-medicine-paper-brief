export function accessStatusLabel(status: string | null | undefined): string {
  switch (status) {
    case "OPEN_ACCESS":
      return "Open access";
    case "ABSTRACT_ONLY":
      return "僅摘要可讀";
    case "INSTITUTIONAL_ACCESS_NEEDED":
      return "需院內/機構權限";
    case "UNKNOWN":
    default:
      return "全文狀態待確認";
  }
}
