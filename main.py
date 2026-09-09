import uuid
import datetime

class AgentIdentity:
    """Represents a digital identity for an 'agent' (e.g., IoT device, microservice)."""
    def __init__(self, agent_type: str):
        self.id = str(uuid.uuid4()) # Unique identifier for the agent identity
        self.agent_type = agent_type # e.g., 'IoT Device', 'Microservice', 'Automation Bot'
        self.status = "CREATED" # Initial status: Doğum (Birth)
        self.owner = None
        self.permissions = set()
        self.creation_date = datetime.datetime.now()
        self.last_updated = self.creation_date
        print(f"[{self.id[:8]}] Agent Identity '{self.agent_type}' created. Status: {self.status}")

    def assign_owner(self, owner_id: str):
        """Assigns an owner to the identity, transitioning to ACTIVE status. Sahiplenme (Ownership)"""
        if self.status == "RETIRED":
            print(f"[{self.id[:8]}] ERROR: Cannot assign owner to a retired identity.")
            return False
        if self.status == "ACTIVE":
            print(f"[{self.id[:8]}] WARNING: Identity already has an owner '{self.owner}'. Reassigning.")
        self.owner = owner_id
        self.status = "ACTIVE" # Identity becomes active upon ownership assignment
        self.last_updated = datetime.datetime.now()
        print(f"[{self.id[:8]}] Agent Identity assigned to owner '{owner_id}'. Status: {self.status}")
        return True

    def add_permission(self, permission: str):
        """Grants a specific permission to the agent identity. Yetki Devri (Authorization)"""
        if self.status != "ACTIVE":
            print(f"[{self.id[:8]}] ERROR: Cannot add permission to an inactive identity. Current status: {self.status}")
            return False
        if permission in self.permissions:
            print(f"[{self.id[:8]}] WARNING: Permission '{permission}' already exists.")
            return False
        self.permissions.add(permission)
        self.last_updated = datetime.datetime.now()
        print(f"[{self.id[:8]}] Permission '{permission}' added.")
        return True

    def delegate_permission(self, permission: str, target_agent_id: str):
        """Simulates delegating a permission to another agent. Yetki Devri (Delegation)"""
        if self.status != "ACTIVE":
            print(f"[{self.id[:8]}] ERROR: Cannot delegate permission from an inactive identity.")
            return False
        if permission not in self.permissions:
            print(f"[{self.id[:8]}] ERROR: Cannot delegate '{permission}': not possessed by this identity.")
            return False
        # In a real system, this would involve creating a temporary credential or
        # updating the target agent's permissions in a central identity store.
        print(f"[{self.id[:8]}] Delegating permission '{permission}' to agent '{target_agent_id[:8]}'.")
        self.last_updated = datetime.datetime.now()
        return True

    def retire(self):
        """Deactivates the agent identity, revoking all permissions. Emeklilik (Retirement)"""
        if self.status == "RETIRED":
            print(f"[{self.id[:8]}] Agent Identity is already retired.")
            return False
        self.status = "RETIRED" # Identity is retired
        self.permissions.clear() # Revoke all permissions upon retirement
        self.owner = None # Clear owner
        self.last_updated = datetime.datetime.now()
        print(f"[{self.id[:8]}] Agent Identity retired. All permissions revoked. Status: {self.status}")
        return True

    def get_info(self):
        """Returns a dictionary of the agent identity's current state."""
        return {
            "id": self.id,
            "agent_type": self.agent_type,
            "status": self.status,
            "owner": self.owner,
            "permissions": list(self.permissions),
            "creation_date": self.creation_date.isoformat(),
            "last_updated": self.last_updated.isoformat()
        }

def main():
    print("--- Simulating Agent Identity Lifecycle ---")

    # 1. Doğum (Birth/Creation) - An identity is born
    print("\n--- Stage 1: Identity Creation (Doğum) ---")
    iot_device_identity = AgentIdentity("IoT Temperature Sensor")
    microservice_identity = AgentIdentity("Payment Gateway Service")

    # 2. Sahiplenme (Ownership/Assignment) - An agent takes ownership of the identity
    print("\n--- Stage 2: Ownership Assignment (Sahiplenme) ---")
    iot_device_identity.assign_owner("SmartHomeSystem-123")
    microservice_identity.assign_owner("BackendTeam-DevOps")

    # Attempt to assign owner to a retired identity (should fail)
    print("\n--- Test: Retire then assign owner ---")
    temp_identity = AgentIdentity("Temporary Bot")
    temp_identity.retire()
    temp_identity.assign_owner("SomeUser") # This should fail as it's retired

    # 3. Yetki Devri (Delegation/Authorization) - Permissions are granted and delegated
    print("\n--- Stage 3: Authorization and Delegation (Yetki Devri) ---")
    iot_device_identity.add_permission("read_temperature_data")
    iot_device_identity.add_permission("send_alerts")
    iot_device_identity.delegate_permission("read_temperature_data", "DataAnalyticsService-456")

    microservice_identity.add_permission("process_payments")
    microservice_identity.add_permission("access_database")
    # Attempt to delegate a permission not held (should fail)
    microservice_identity.delegate_permission("manage_users", "AdminService-789")
    microservice_identity.delegate_permission("access_database", "AuditService-001")

    # 4. Emeklilik (Retirement/Deactivation) - The identity is retired
    print("\n--- Stage 4: Identity Retirement (Emeklilik) ---")
    print("\n--- Current state of IoT Device Identity before retirement ---")
    print(iot_device_identity.get_info())
    iot_device_identity.retire()
    print("\n--- State after IoT Device Identity retirement ---")
    print(iot_device_identity.get_info())

    print("\n--- Current state of Microservice Identity (still active) ---")
    print(microservice_identity.get_info())
    microservice_identity.add_permission("log_transactions") # Should work as it's still active
    print("\n--- State after Microservice Identity adds new permission (still active) ---")
    print(microservice_identity.get_info())

    print("\n--- Attempting to add permission to retired identity (should fail) ---")
    iot_device_identity.add_permission("update_firmware") # This should fail

    print("\n--- Agent Identity Lifecycle Simulation Complete ---")

if __name__ == "__main__":
    main()
