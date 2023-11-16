from objects.staff import Staff
from settings.string_constants import COLOR
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING, StaffAttributesDicts
if TYPE_CHECKING:
    from widgets.graphboard.graphboard import GraphBoard

class GhostStaff(Staff):
    def __init__(self, graphboard: 'GraphBoard', attributes: StaffAttributesDicts) -> None:
        super().__init__(graphboard, attributes)
        self.setOpacity(0.2)        
        self.graphboard = graphboard
        self.target_staff = None
