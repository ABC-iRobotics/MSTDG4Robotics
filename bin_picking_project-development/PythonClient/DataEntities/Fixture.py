class Fixture:

    def __init__(self, abs_pos, abs_or, rel_pos, rel_or, size):
        self.absolutePosition = abs_pos
        self.absoluteOrientation = abs_or
        self.relativePosition = rel_pos
        self.relativeOrientation = rel_or
        self.size = size
    
    def dictMapper(self):
        return  {
                    'absolutePosition': self.absolutePosition, 
                    'absoluteOrientation': self.absoluteOrientation,
                    'relativePosition': self.relativePosition,
                    'relativeOrientation': self.relativeOrientation,
                    'size': self.size
                }

