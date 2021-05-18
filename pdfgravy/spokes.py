from .nest import Nest, Nested

class Spokes(Nest):

    class Decorators:

        @classmethod
        def add_spoke(decs, func):
            """
            Quick shorthand for adding spokes to the nest.
            """
            def inner(cls, *args, **kwargs):
                for elem in func(cls, *args, **kwargs):
                    cls.append(elem)
            return inner

    @Decorators.add_spoke
    def add_vertical(self, lbl, data, words):
        """
        Add vertical spokes splitting into sub-spokes as required.
        """
        if len(data) < 2:  # True if only one spoke --> no splitting
            yield Spoke([lbl], data, orientation='v', val=data.midx)
        else:
            for sub in data:
                
                # Do x-filtering then find area above col/below label
                lbls = words.filter(Nested.chk_intersection, sub, x_only=True)
                lbls = lbls.slice(y0=sub.y1, y1=lbl.y0)

                yield Spoke([lbl, *lbls], sub, orientation='v', val=sub.midx)  

    @Decorators.add_spoke
    def add_horizontal(self, lbl, data, h_lbls):
        """
        Add horizontal spokes consolidating aggregates as necessary
        """
        lbls = [lbl]
        for x in [x for y in h_lbls for x in y]:  # Iterate over flattened list
            if not x.chk_intersection(lbl, y_only=True) or x in lbls:
                continue
            lbls.append(x)
        yield Spoke(lbls, data, orientation='h', val=data.midx)

class Spoke:

    def __init__(self, lbls, data, orientation, val):
        """
        Store constitutive spoke and label data. 
        """
        self.orientation = orientation
        self.val = val

        if orientation == 'h':
            self.lbls = sorted(lbls, key=lambda x: x.x0)
        else:
            self.lbls = sorted(lbls, key=lambda x: x.y0, reverse=True)

        self.title = ', '.join([x.text.strip('\n ') for x in self.lbls])
        
        self.debug = data

    def __repr__(self):
        return f'{self.title}: {self.val} ({self.orientation})'