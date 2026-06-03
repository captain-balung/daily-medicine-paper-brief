from workers.shared.config import load_settings


def main() -> None:
    settings = load_settings()
    checks = settings.health_checks()

    print("worker=ok")
    for name, ok in checks.items():
        status = "pass" if ok else "missing"
        print(f"{name}={status}")


if __name__ == "__main__":
    main()
