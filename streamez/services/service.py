class IService:
    def should_skip(self) -> bool:
        """
        Return true if this service should be skipped.
        """
        pass

    def initialize(self) -> bool:
        """
        Initialize the service.
        """
        pass

    def start(self) -> bool:
        """
        Start the service.
        """
        pass

    def stop(self) -> bool:
        """
        Stop the service.
        """
        pass

    def reload(self) -> bool:
        """
        Reload the service.
        """
        pass