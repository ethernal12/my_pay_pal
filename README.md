# New service protocol

* Define contract!
* Define contract implementation.
* Connect with APP arhitecture (service_provider.py)
* Connect new service in usecases where you need one!

# New use case protocol

* Define usecase implementation. (use only stuff from inside of class)
* Define all services that you need with dataclass properties.
* Connect new usecase in usecase provider!

# Your JOB

* Implement service in app/services
* Implement usecase in core/usecases