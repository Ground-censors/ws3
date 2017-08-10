import sys
import re
import copy
import operator
import random
from itertools import chain
_cfi = chain.from_iterable
from collections import defaultdict as dd

try:
    from . import common
    from . import core
except: # "__main__" case
    import common
    import core
from common import timed
    
#_mad = common.MAX_AGE_DEFAULT

class GreedyAreaSelector:
    """
    Selects area for treatment from oldest age classes.
    """
    def __init__(self, parent):
        self.parent = parent

    def operate(self, period, acode, target_area, mask=None,
                commit_actions=True, verbose=False):
        """
        Greedily operate on oldest operable age classes.
<<<<<<< HEAD
        Returns missing area (i.e., difference between target and operated areas).
=======
        Return missing area.
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        """
        wm = self.parent
        key = lambda item: max(item[1])
        odt = sorted(wm.operable_dtypes(acode, period, mask).items(), key=key)
        print ' entering selector.operate()', len(odt), 'operable dtypes'
<<<<<<< HEAD
=======
        for dtk, ages in odt:
            print dtk, ages[-1], wm.dtypes[dtk].operable_area(acode, period, ages[-1])
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        while target_area > 0 and odt:
            while target_area > 0 and odt:
                popped = odt.pop()
                try:
                    dtk, ages = popped #odt.pop()
                except:
                    print odt
                    print popped
                    raise
                age = sorted(ages)[-1]
                oa = wm.dtypes[dtk].operable_area(acode, period, age)
                if not oa: continue # nothing to operate
                area = min(oa, target_area)
                target_area -= area
                if area < 0:
                    print 'negative area', area, oa, target_area, acode, period, age
                    assert False
                if verbose:
                    print ' selector found area', [' '.join(dtk)], acode, period, age, area
<<<<<<< HEAD
                wm.apply_action(dtk, acode, period, age, area)
=======
                wm.apply_action(dtk, acode, period, age, area, verbose=verbose)
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
            odt = sorted(wm.operable_dtypes(acode, period).items(), key=key)
        wm.commit_actions(period, repair_future_actions=True)
        if verbose:
            print 'GreedyAreaSelector.operate done (remaining target_area: %0.1f)' % target_area
        return target_area
    
class Action:
<<<<<<< HEAD
    """
    Encapsulates data for an action.
    """
    
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
    def __init__(self,
                 code,
                 targetage=None,
                 descr='',
                 lockexempt=False,
                 #oper_expr='',
                 components=None,
                 partial=None):
        self.code = code
        self.targetage = targetage
        self.descr = descr
        self.lockexempt = lockexempt
        self.oper_a = None 
        self.oper_p = None
        #self.oper_expr = oper_expr
        self.components = components or []
        self.partial = partial or []
        self.is_compiled = False
        self.is_harvest = 0
        self.treatment_type = None
    
class DevelopmentType:
    """
<<<<<<< HEAD
    Encapsulates Woodstock development type data (curves, age, area), and provides methods to operate on the data.
=======
    Encapsulates Woodstock development type (curves, age, area).
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
    """
    _bo = {'AND':operator.and_, '&':operator.and_, 'OR':operator.or_, '|':operator.or_}
    
    def __init__(self,
                 key,
                 parent):
<<<<<<< HEAD
        """
        The key is basically the fully expanded mask (expressed as a tuple of values). The parent is a reference to the WoodstockModel object in which self is embedded.
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        self.key = key
        self.parent = parent
        self._rc = parent.register_curve # shorthand
        self._max_age = parent.max_age
        self._ycomps = {}
        self._complex_ycomps = {}
        self._zero_curve = parent.common_curves['zero']
        self._unit_curve = parent.common_curves['unit']
        self._ages_curve = parent.common_curves['ages']                           
        self._resolvers = {'MULTIPLY':self._resolver_multiply,
                           'DIVIDE':self._resolver_divide,
                           'SUM':self._resolver_sum,
                           'CAI':self._resolver_cai,
                           'MAI':self._resolver_mai,
                           'YTP':self._resolver_ytp,
                           'RANGE':self._resolver_range}
        self.transitions = {} # keys are (acode, age) tuples
        #######################################################################
        # Use period 0 slot to store starting inventory.
        self._areas = {p:dd(float) for p in range(0, self.parent.horizon+1)}
        #######################################################################
        self.oper_expr = dd(list)
        self.operability = {}

    def operable_ages(self, acode, period):
<<<<<<< HEAD
        """
        Finds list of ages at which self is operable, given an action code and period index.
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        if acode not in self.oper_expr: # action not defined for this development type
            return None
        if acode not in self.operability: # action not compiled yet...
            if self.compile_action(acode) == -1: return None # never operable
        #print ' '.join(self.key), acode, period, self.operability, self.oper_expr
        if period not in self.operability[acode]:
            return None
        else:
            lo, hi = self.operability[acode][period]
            return list(set(range(lo, hi+1)).intersection(self._areas[period].keys()))        
    
    def is_operable(self, acode, period, age=None):
        """
        Test hypothetical operability.
        Does not imply that there is any operable area in current inventory.
        """
        if acode not in self.oper_expr: # action not defined for this development type
            print self.oper_expr
            return False
        if acode not in self.operability: # action not compiled yet...
            if self.compile_action(acode) == -1:
                print 'never operable', acode
                return False # never operable
        if period not in self.operability[acode]:
            print acode, period
            assert False
            return False
        else:
            lo, hi = self.operability[acode][period]
            #print 'is_operable', acode, period, age, hi, lo
            return age >= lo and age <= hi
        
    def operable_area(self, acode, period, age=None, cleanup=True):
        """
<<<<<<< HEAD
        Returns 0 if inoperable or no current inventory, operable area given action code and period (and optionally age) index otherwise. If cleanup switch activated (default True) and age specified, deletes the ageclass from the inventory dict if operable area is less than self.parent.area_epsilon. 
=======
        Returns 0. if inoperable or no current inventory. 
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        """
        if acode not in self.oper_expr: # action not defined for this development type
            return 0.
        if acode not in self.operability: # action not xf yet...
            if self.compile_action(acode) == -1: return 0. # never operable
        if age is None: # return total operable area
            return sum(self.operable_area(acode, period, a) for a in self._areas[period].keys())
        if age not in self._areas[period]:
            # age class not in inventory
            return 0.
        elif abs(self._areas[period][age]) < self.parent.area_epsilon:
            # negligible area
            #print 'no area', acode, period, age, self._areas[period][age]
            #print ' '.join(self.key)
            #print self._areas[period].keys()
            if cleanup: # remove ageclass from dict (frees up memory)
                del self._areas[period][age]
            return 0.
        elif self.is_operable(acode, period, age):
            #print 'operable', acode, period, age #, self.operability[acode]
            return self._areas[period][age]
        else:
            return 0.
        assert False
                
    def area(self, period, age=None, area=None, delta=True):
<<<<<<< HEAD
        """
        If area not specified, returns area inventory for period (optionally age), else sets area for period and age. If delta switch active (default True), area value is interpreted as an increment on current inventory.
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        #if area is not None:
        #    print area
        #    assert area > 0
        if area is None: # return area for period and age
            if age is not None:
                try:
                    return self._areas[period][age]
                except:
                    return 0.
            else: # return total area
                return sum(self._areas[period][a] for a in self._areas[period])
        else: 
            if delta:
                self._areas[period][age] += area
            else:
                self._areas[period][age] = area
        
    def resolve_condition(self, yname, lo, hi):
<<<<<<< HEAD
        """
        Find lower and upper ages that correspond to lo and hi values of yname (interpreted as first occurence of yield value, reading curve from left and right, respectively).
        """
        return [x for x, y in enumerate(self.ycomp(yname)) if y >= lo and y <= hi]
       
    def reset_areas(self, period=None):
        """
        Reset areas dict.
        """
=======
        return [x for x, y in enumerate(self.ycomp(yname)) if y >= lo and y <= hi]
       
    def reset_areas(self, period=None):
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        periods = self.parent.periods if period is None else [period]
        for period in periods:
            self._areas[period] = dd(float)

    def ycomps(self):
<<<<<<< HEAD
        """
        Returns list of yield component keys.
        """
        return self._ycomps.keys()
            
    def ycomp(self, yname, silent_fail=True):
        """
        Returns yield component, given key (default returns None on invalid key).
        """
=======
        return self._ycomps.keys()
            
    def ycomp(self, yname, silent_fail=True):
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        if yname in self._ycomps:
            if not self._ycomps[yname]: # complex ycomp not compiled yet
                self._compile_complex_ycomp(yname)
            return self._ycomps[yname]
        else: # not a valid yname
            if silent_fail:
                return None 
            else: 
                 raise KeyError("ycomp '%s' not in development type '%s'" % (yname, ' '.join(self.key)))
                    
    def _o(self, s, default_ycomp=None): # resolve string operands
        if not default_ycomp: default_ycomp = self._zero_curve
        if common.is_num(s):
            return float(s)
        elif s.startswith('#'):
            return self.parent.constants[s[1:]]
        else:
            s = s.lower() # just to be safe
            ycomp = self.ycomp(s)
            return ycomp if ycomp else default_ycomp
        
    def _resolver_multiply(self, yname, d):
        args = [self._o(s.lower()) for s in re.split('\s?,\s?', re.search('(?<=\().*(?=\))', d).group(0))]
        ##################################################################################################
        # NOTE: Not consistent with Remsoft documentation on 'complex-compound yields' (fix me)...
        ytype_set = set(a.type for a in args if isinstance(a, core.Curve))
        return ytype_set.pop() if len(ytype_set) == 1 else 'c', self._rc(reduce(lambda x, y: x*y, args))
        ##################################################################################################

    def _resolver_divide(self, yname, d):
        _tmp = zip(re.split('\s?,\s?', re.search('(?<=\().*(?=\))', d).group(0)),
                   (self._zero_curve, self._unit_curve))
        args = [self._o(s, default_ycomp) for s, default_ycomp in _tmp]
        return args[0].type if not args[0].is_special else args[1].type, self._rc(args[0] / args[1])
        
    def _resolver_sum(self, yname, d):
        args = [self._o(s.lower()) for s in re.split('\s?,\s?', re.search('(?<=\().*(?=\))', d).group(0))] 
        ytype_set = set(a.type for a in args if isinstance(a, core.Curve))
        return ytype_set.pop() if len(ytype_set) == 1 else 'c', self._rc(reduce(lambda x, y: x+y, [a for a in args]))
        
    def _resolver_cai(self, yname, d):
        arg = self._o(re.split('\s?,\s?', re.search('(?<=\().*(?=\))', d).group(0))[0])
        return arg.type, self._rc(arg.mai())
        
    def _resolver_mai(self, yname, d):
        arg = self._o(re.split('\s?,\s?', re.search('(?<=\().*(?=\))', d).group(0))[0])
        return arg.type, self._rc(arg.mai())
        
    def _resolver_ytp(self, yname, d):
        arg = self._o(re.search('(?<=\().*(?=\))', d).group(0).lower())
        return arg.type, self._rc(arg.ytp())
        
    def _resolver_range(self, yname, d):
        args = [self._o(s.lower()) for s in re.split('\s?,\s?', re.search('(?<=\().*(?=\))', d).group(0))] 
        arg_triplets = [args[i:i+3] for i in xrange(0, len(args), 3)]
        range_curve = self._rc(reduce(lambda x, y: x*y, [t[0].range(t[1], t[2]) for t in arg_triplets]))
        #print ' '.join(self.key), yname, range_curve.points()
        return args[0].type, self._rc(reduce(lambda x, y: x*y, [t[0].range(t[1], t[2]) for t in arg_triplets]))

    def _compile_complex_ycomp(self, yname):
        expression = self._complex_ycomps[yname]
        keyword = re.search('(?<=_)[A-Z]+(?=\()', expression).group(0)
        #print 'compiling complex', yname, keyword
        try:
            ytype, ycomp = self._resolvers[keyword](yname, expression)
            ycomp.label = yname
            ycomp.type = ytype
            self._ycomps[yname] = ycomp 
        except KeyError:
                raise ValueError('Problem compileing complex yield: %s, %s' % (yname, expression))
            
    def compile_actions(self, verbose=False):
<<<<<<< HEAD
        """
        Compile all actions.
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        for acode in self.oper_expr:
            self.compile_action(acode, verbose)

    def compile_action(self, acode, verbose=False):
<<<<<<< HEAD
        """
        Compile action, given action code. 
        This mostly involves resolving operability expression strings into
        lower and upper operability limits, defined as (alo, ahi) age pair for each period.
        Deletes action from self if not operable in any period.
        """
=======
        #print 'compiling action'
        #print ' '.join(self.key), acode
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        self.operability[acode] = {}
        for expr in self.oper_expr[acode]:
            self._compile_oper_expr(acode, expr, verbose)
        is_operable = False
        for p in self.operability[acode]:
            if self.operability[acode][p] is not None:
                #print 'compile_action', expr, acode, p, self.operability[acode][p]
                is_operable = True
        if not is_operable:
            if verbose: print 'not operable (deleting):', acode
            del self.operability[acode]
            del self.oper_expr[acode]
            return -1
        else:
            if verbose: print 'operable:', acode #, self.operability[acode]
        return 0
            
    def _compile_oper_expr(self, acode, expr, verbose=False):
        expr = expr.replace('&', 'and').replace('|', 'or')
        oper = None
        plo, phi = 1, self.parent.horizon # count periods from 1, as in Woodstock...
        alo, ahi = 0, self._max_age 
        if 'and' in expr:
            oper = 'and'
        elif 'or' in expr:
            oper = 'or'
            alo, ahi = self._max_age+1, -1
        cond_comps = expr.split(' %s ' % oper)
        lhs, rel_operators, rhs = zip(*[cc.split(' ') for cc in cond_comps])
        rhs = map(float, rhs)
        _plo, _phi, _alo, _ahi = None, None, None, None
        for i, o in enumerate(lhs):
            if o == '_cp':
                #print 'rhs', rhs
                period = int(rhs[i])
                assert period <= self.parent.horizon # sanity check
                #################################################################
                # Nonsense to relate time-based and age-based conditions with OR?
                # Recondider if this actually ever comes up...
                assert oper != 'or'  
                #################################################################
                if rel_operators[i] == '=':
                    _plo, _phi = period, period
                elif rel_operators[i] == '>=':
                    _plo = period
                elif rel_opertors[i] == '<=':
                    _phi = period
                else:
                    raise ValueError('Bad relational operator.')
                plo, phi = max(_plo, plo), min(_phi, phi)
            elif o == '_age':
                age = int(rhs[i])
                if rel_operators[i] == '=':
                    _alo, _ahi = age, age
                elif rel_operators[i] == '>=':
                    _alo = age
                elif rel_operators[i] == '<=':
                    _ahi = age
                else:
                    raise ValueError('Bad relational operator.')                    
            else: # must be yname
                ycomp = self.ycomp(o)
                if rel_operators[i] == '=':
                    _alo = _ahi = ycomp.lookup(rhs[i])
                elif rel_operators[i] == '>=':
                    #print ' ge', o, ycomp[45], ycomp.lookup(0)  
                    _alo = ycomp.lookup(rhs[i])
                elif rel_operators[i] == '<=':
                    #print ' le', o 
                    _ahi = ycomp.lookup(rhs[i])
                else:
                    raise ValueError('Bad relational operator.')
                #print ' ', o, (alo, _alo), (ahi, _ahi)
            if oper == 'and':
                if _alo is not None: alo = max(_alo, alo)
                if _ahi is not None: ahi = min(_ahi, ahi)
            else: # or
                if _alo is not None: alo = min(_alo, alo)
                if _ahi is not None: ahi = max(_ahi, ahi)
        if plo > phi:
<<<<<<< HEAD
            print plo, phi
            assert plo <= phi # should never explicitly declare infeasible period range...
        for p in range(plo, phi+1):
            self.operability[acode][p] = (alo, ahi) if alo <= ahi else None 
                
    def add_ycomp(self, ytype, yname, ycomp, first_match=True):
        """
        Add yield component.
        """
=======
            #print plo, phi
            assert plo <= phi # should never explicitly declare infeasible period range...
        for p in range(plo, phi+1):
            #print alo, ahi
            self.operability[acode][p] = (alo, ahi) if alo <= ahi else None 
                
    def add_ycomp(self, ytype, yname, ycomp, first_match=True):
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        if first_match and yname in self._ycomps: return # already exists (reject)
        if ytype == 'c':
            self._complex_ycomps[yname] = ycomp
            self._ycomps[yname] = None
        if isinstance(ycomp, core.Curve):
            self._ycomps[yname] = ycomp
    
    def grow(self, start_period=1, cascade=True):
<<<<<<< HEAD
        """
        Grow self (default starting period 1, and cascading to end of planning horizon).
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        end_period = start_period + 1 if not cascade else self.parent.horizon
        for p in range(start_period, end_period):
            self.reset_areas(p+1), self._areas[p], self._areas[p+1]
            for age, area in self._areas[p].items(): self._areas[p+1][age+1] = area

    def initialize_areas(self):
<<<<<<< HEAD
        """
        Copy initial inventory to period-1 inventory.
        """
        self._areas[1] = copy.copy(self._areas[0])
        
class Output:
    """
    Encapsulates data and methods to operate on aggregate outputs from the model.
    Emulates behaviour of Woodstock outputs.
    .. warning:: Behaviour of Woodstock outputs is quite complex. This class needs more work before it is used in a production setting (i.e., resolution of some complex output cases is buggy).
    """
=======
        self._areas[1] = copy.copy(self._areas[0])
        
class Output:
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
    def __init__(self,
                 parent,
                 code=None,
                 expression=None,
                 factor=(1., 1),
                 description='',
                 theme_index=-1,
                 is_basic=False,
                 is_level=False):
        self.parent = parent
        self.code = code
        self.expression = expression
        self._factor = factor
        self.description = description
        self.theme_index = theme_index
        self.is_themed = True if theme_index > -1 else False 
        self.is_basic = is_basic
        if is_basic:
            self._compile_basic(expression) # shortcut
        elif not is_level:
            self._compile(expression) # will detect is_basic
        self.is_level = is_level

    def _lval(self, s):
        """
        Resolve left operand in sub-expression.
        """
        if s.lower() in self.parent.outputs:
            return self.parent.outputs[s.lower()]
        else: # expression
            return s.lower()

    def _rval(self, s): 
        """
        Resolve right operand in sub-expression.
        """
        if common.is_num(s):
            return float(s)
        elif s.startswith('#'):
            return self.parent.constants[s[1:].lower()]
        else: # time-based ycomp code
            return s.lower()
            
    def _compile(self, expression):
        """
        Resolve operands in expression to the extent possible.
        Can be basic or summary.
        Assuming operand pattern:
          lval_1 [*|/ rval_1] +|- .. +|- lval_n [*|/ rval_n]
        where
          lval := ocode or expression
          rval := number or #constant or ycomp
        """
        t = re.split(r'\s+(\+|-)\s+', expression)
        ocomps = t[::2]  # output component sub-expressions
        signs = [1.] # implied + in front of expression
        signs.extend(1. if s == '+' else -1 for s in t[1::2]) 
        factors = [(1., 1) for i in ocomps]
        for i, s in enumerate(ocomps):
            tt = re.split(r'\s+(\*|/)\s+', s) # split on */ operator
            lval = self._lval(tt[0])
            if len(tt) > 1:
                factors[i] = self._rval(tt[2]), 1 if tt[1] == '*' else -1
            if not isinstance(lval, Output):     
                if len(ocomps) == 1: # simple basic output (special case)
                    self.is_basic = True
                    self._factor = factors[0]
                    self._compile_basic(lval)
                    return
                else: # compound basic output
                    ocomps[i] = Output(parent=self.parent,
                                       expression=lval,
                                       factor=factors[i],
                                       is_basic=True)
            else: # summary output
                ocomps[i] = lval #self.parent.outputs[lval]
        self._ocomps = ocomps
        self._signs = signs
        self._factors = factors

    def _compile_basic(self, expression):
        # clean up (makes parsing easier)
        s = re.sub('\s+', ' ', expression) # separate tokens by single space
        s = s.replace(' (', '(')  # remove space to left of left parentheses
        t = s.lower().split(' ')
        # filter dtypes, if starts with mask
        mask = None
        if not (t[0] == '@' or t[0] == '_' or t[0] in self.parent.actions):
            mask = tuple(t[:self.parent.nthemes])
            t = t[self.parent.nthemes:] # pop
        #try:
        #print expression
        self._dtype_keys = self.parent.unmask(mask) if mask else self.parent.dtypes.keys()
        #except:
        #    print expression
        #    assert False
        # extract @AGE or @YLD condition, if present
        self._ages = None
        self._condition = None
        if t[0].startswith('@age'):
            lo, hi = [int(a)+i for i, a in enumerate(t[0][5:-1].split('..'))]
            hi = min(hi, self.parent.max_age+1) # they get carried away with range bounds...
            self._ages = range(lo, hi)
            t = t[1:] # pop
        elif t[0].startswith('@yld'):
            ycomp, args = t[0][5:-1].split(',')
            self._condition = tuple([ycomp] + [float(a) for a in args.split('..')])
            self._ages = None
            t = t[1:] # pop
        if not self._ages and not self._condition: self._ages = self.parent.ages
        # extract _INVENT or acode
        if t[0].startswith('_'): # _INVENT
            self._is_invent = True
            self._invent_acodes = t[0][8:-1].split(',') if len(t[0]) > 7 else None
            self._acode = None
        else: # acode
            self._is_invent = False
            self._invent_acodes = None
            self._acode = t[0]
        t = t[1:] # pop
        # extract _AREA or ycomp
        if t[0].startswith('_'): # _AREA
            self._is_area = True
            self._ycomp = None
        else: # acode
            self._is_area = False
            self._ycomp = t[0]
        t = t[1:] # pop

    def _evaluate_basic(self, period, factors, verbose=0, cut_corners=True):
        result = 0.
        if self._invent_acodes:
            acodes = [acode for acode in self._invent_acodes if parent.applied_actions[period][acode]]
            if cut_corners and not acodes:
                return 0. # area will be 0...
        for k in self._dtype_keys:
            dt = self.parent.dtypes[k]
            if cut_corners and not self._is_invent and k not in self.parent.applied_actions[period][self._acode]:
                if verbose: print 'bailing on', period, self._acode, ' '.join(k)
                continue # area will be 0...
            if isinstance(self._factor[0], float):
                f = pow(*self._factor)
            else:
                f = pow(dt.ycomp(self._factor[0])[period], self._factor[1])
            for factor in factors:
                if isinstance(factor[0], float):
                    f *= pow(*factor)
                else:
                    f *= pow(dt.ycomp(factor[0])[period], factor[0])
            if cut_corners and not f:
                if verbose: print 'f is null', f
                continue # one of the factors is 0, no point calculating area...
            ages = self._ages if not self._condition else dt.resolve_condition(*self._condition)
            for age in ages:
                area = 0.
                if self._is_invent:
                    if cut_corners and not dt.area(period, age):
                        continue
                    if self._invent_acodes:
                        any_operable = False
                        for acode in acodes:
                            if acode not in dt.operability: continue
                            if dt.is_operable(acode, period, age):
                                any_operable = True
                        if any_operable:
                            area += dt.area(period, age)
                    else:
                        area += dt.area(period, age)
                else:
                    assert False # not implemented yet...
                y = 1. if self._is_area else dt.ycomp(self._ycomp)[age]
                result += y * area * f
        return result

    def _evaluate_summary(self, period, factors):
        result = 0.
        for i, ocomp in enumerate(self._ocomps):
            result += ocomp(period, [self._factors[i]] + factors)
        return result

    def _evaluate_basic_themed(self, period):
        pass

    def _evaluate_summed_themed(self, period):
        pass
            
    def __call__(self, period, factors=[(1., 1)]):
        if self.is_basic:
            return self._evaluate_basic(period, factors)
        else:
            return self._evaluate_summary(period, factors)

    def __add__(self, other):
        # assume Output + Output
        if self.is_themed:
            return [i + j for i, j in zip(self(), other())]
        else:
            return self() + other()

    def __sub__(self, other):
        # assume Output - Output 
        if self.is_themed:
            return [i - j for i, j in zip(self(), other())]
        else:
            return self() - other()

class WoodstockModel:
    """
    Interface to import Woodstock models.
<<<<<<< HEAD
    Also includes methods to simulate growth, applying actions.
    Includes methods to query the model post-simulation (i.e., workaround for broken Outputs class).
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
    """
    _ytypes = {'*Y':'a', '*YT':'t', '*YC':'c'}
    tree = (lambda f: f(f))(lambda a: (lambda: dd(a(a))))
    #_vp_ratio_default = 1.
    #_piece_size_yname_default = 'yd3s'
    #_piece_size_factor_default = 0.001 # convert cubic decimeters to cubic meters
    #_total_volume_yname_default = 'yv_s'

            
    def __init__(self,
                 model_name,
                 model_path,
                 horizon=common.HORIZON_DEFAULT,
                 period_length=common.PERIOD_LENGTH_DEFAULT,
                 max_age=common.MAX_AGE_DEFAULT,
                 #species_groups=common.SPECIES_GROUPS_WOODSTOCK_QC, # not used (DELETE) [commenting out]
                 area_epsilon=common.AREA_EPSILON_DEFAULT,
                 curve_epsilon=common.CURVE_EPSILON_DEFAULT):
                 #vp_ratio=_vp_ratio_default,
                 #piece_size_yname=_piece_size_yname_default,
                 #piece_size_factor=_piece_size_factor_default,
                 #total_volume_yname=_total_volume_yname_default):
        self.model_name = model_name
        self.model_path = model_path
        self.horizon = horizon
        self.periods = range(1, horizon+1)
        self.period_length = period_length
        self.max_age = max_age
        self.ages = range(max_age+1)
        #self._species_groups = species_groups # Not used (DELETE) [commenting out]
        self.yields = []
        self.ynames = set()
        self.actions = {}
        self.transitions = {}
        self.oper_expr = {}
        self._themes = []
        self._theme_basecodes = []
        self.dtypes = {}
        self.constants = {}
        self.output_groups = {}
        self.outputs = {}        
        self.reset_actions()
        self.curves = {}
        c_zero = self.register_curve(core.Curve('zero',
                                                is_special=True,
                                                type=''))
        c_unit = self.register_curve(core.Curve('unit',
                                                points=[(0, 1)],
                                                is_special=True,
                                                type=''))
        c_ages = self.register_curve(core.Curve('ages',
                                                points=[(0, 0), (max_age, max_age)],
                                                is_special=True,
                                                type='')) 
        self.common_curves = {'zero':c_zero,
                              'unit':c_unit,
                              'ages':c_ages}
        self.area_epsilon = area_epsilon
        self.curve_epsilon = curve_epsilon
        self.areaselector = GreedyAreaSelector(self)
        self.inoperable_dtypes = []
        #self._vp_ratio = vp_ratio
        #self.piece_size_yname = piece_size_yname
        #self.piece_size_factor = piece_size_factor
        #self.total_volume_yname = total_volume_yname

    def is_harvest(self, acode):
<<<<<<< HEAD
        """
        Returns True if acode corresponds to a harvesting action.
        """
        return self.actions[acode].is_harvest
        
    def piece_size(self, dtype_key, age):
        """
        Returns piece size, given development type key and age.
        """
        return self.dtypes[dtype_key].ycomp(self.piece_size_yname)[age] * self.piece_size_factor

    def dt(self, dtype_key):
        """
        Returns development type, given key (returns None on invalid key).
        """
=======
        return self.actions[acode].is_harvest
        
    def piece_size(self, dtype_key, age):
        return self.dtypes[dtype_key].ycomp(self.piece_size_yname)[age] * self.piece_size_factor

    def dt(self, dtype_key):
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        try:
            return self.dtypes[dtype_key]
        except:
            return None

    def age_class_distribution(self, period, mask=None):
<<<<<<< HEAD
        """
        Returns age class distribution (dict of areas, keys on age).
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        result = {age:0. for age in self.ages}
        dtype_keys = self.unmask(mask) if mask else self.dtypes.keys()
        for dtk in dtype_keys:
            dt = self.dtypes[dtk]
            for age in dt._areas[period]:
                result[age] += dt._areas[period][age]
        return result
           
    def operable_dtypes(self, acode, period, mask=None):
<<<<<<< HEAD
        """
        Returns dict (keyed on development type key, values are lists of operable ages).
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        result = {}
        dtype_keys = self.unmask(mask) if mask else self.dtypes.keys()
        for dtk in dtype_keys:
            dt = self.dtypes[dtk]
            operable_ages = dt.operable_ages(acode, period)
            if operable_ages:
<<<<<<< HEAD
                result[dt.key] = operable_ages
        return result

    def inventory(self, period, yname=None, age=None, mask=None):
        """
        Flexible method that compiles inventory at given period.
        Unit of return data defaults to area if yname not given, but takes on unit of yield component otherwise. Can be constrained by age and development type mask.
        """
=======
                result[dt.key] = [oa for oa in operable_ages if dt.area(period, oa)]
        return result

    def inventory(self, period, yname=None, age=None, mask=None):
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        result = 0.
        dtype_keys = self.unmask(mask) if mask else self.dtypes.keys()
        for dtk in dtype_keys:
            dt = self.dtypes[dtk]
            if yname:
                ycomp = dt.ycomp(yname)
                if age:
                    result += dt.area(period, age) * ycomp[age]
                else:
                    result += sum(dt.area(period, a) * ycomp[a] for a in dt._areas[period])
            else:
                result += dt.area(period, age)
        return result
        
    def operable_area(self, acode, period, age=None):
<<<<<<< HEAD
        """
        Returns total operable area, given action code and period (and optionally age).
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        return sum(dt.operable_area(acode, period, age) for dt in self.dtypes.values())
        
    def initialize_areas(self):
        """
        Copies areas from period 0 to period 1.
        """
        for dt in self.dtypes.values(): dt.initialize_areas()
        
    def register_curve(self, curve):
<<<<<<< HEAD
        """
        Add curve to global curve hash map (uses result of Curve.points() to construct hash key). 
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        key = tuple(curve.points())
        if key not in self.curves:
            # new curve (lock and register)
            curve.is_locked = True # points list must not change, else not valid key
            self.curves[key] = curve
        return self.curves[key]
            
    # def _rdd(self):
    #     """
    #     Recursive defaultdict (i.e., tree)
    #     """
    #     return dd(self._rdd)   
    
<<<<<<< HEAD
    def reset_actions(self, period=None, acode=None):
        """
        Resets actions (default resets all periods, all actions, unless period or acode specified).
        """
=======
    def reset_actions(self, period=None, acode=None):       
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        if period is None:
            print "resetting actions"
            self.applied_actions = {p:{acode:{} for acode in self.actions.keys()} for p in self.periods}
        else:
            if acode is None:
                # NOTE: This DOES NOT deal with consequences in future periods...
                self.applied_actions[period] = {acode:{} for acode in self.actions.keys()}
            else:
                assert period is not None
                self.applied_actions[period][acode] = {}

    # def reset_actions(self, period=None, acode=None):
    #     if period is None:
    #         self.applied_actions = {p:self._rdd() for p in self.periods}
    #     else:
    #         if acode is None:
    #             # NOTE: This DOES NOT deal with consequences in future periods...
    #             self.applied_actions[period] = self._rdd()
    #         else:
    #             assert period is not None
    #             self.applied_actions[period][acode] = self._rdd()

    def compile_product(self,
                        period,
                        expr,
                        acode=None,
                        dtype_keys=None,
                        age=None,
                        verbose=False):
<<<<<<< HEAD
        """
        Compiles products from applied actions in given period. Parses string expression, which resolves to a single coefficient. Operated area can be filtered on action code, development type key list, and age. Result is product of sum of filtered area and coefficient. 
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        aa = self.applied_actions
        if acode is None:
            acodes = self.actions.keys()
        else:
            acodes = [acode] if not self.actions[acode].components else self.actions[acode].components
        tokens = expr.split(' ')
        result = 0.
        for _acode in acodes:
            #if not aa[period][_acode]: continue # acode not in solution
            if _acode not in aa[period].keys(): continue # acode not in solution
            _dtype_keys = aa[period][_acode].keys() if dtype_keys is None else dtype_keys
            #print 'compile_product len(dtype_keys)', len(dtype_keys)
            #keep = 0
            #skip = 0
            for dtk in _dtype_keys:
                if dtk not in aa[period][_acode].keys():
                    #skip += 1
                    #if verbose: print len(aa[period][_acode].keys()), dtk 
                    continue
                #keep += 1
                ages = aa[period][_acode][dtk].keys() if age is None else [age]
                for _age in ages:
                    aaa = aa[period][_acode][dtk][_age]
                    _tokens = []
                    for token in tokens:
                        if token in self.ynames: # found reference to ycomp
                            if token in aaa[1]: # token is yname in products (replace with value)
                                _tokens.append(str(aaa[1][token]))
                            else: # assume null value if ycomp exists but not stored in solution
                                _tokens.append('0.')
                        else:
                            _tokens.append(token)
                    _expr = ' '.join(_tokens)
                    #print "evaluating expression '%s' for case:" % ' '.join(_tokens), [' '.join(dtk)], _acode, _age
                    try:
                        result += eval(_expr) * aaa[0]
                    except ZeroDivisionError:
                        pass # let this one go...
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        print "evaluating expression '%s' for case:" % ' '.join(_tokens), period, [' '.join(dtk)], _acode, _age
                        raise

            #print _acode, 'keep', keep, 'skip', skip
        return result
        
                
    def operated_area(self, acode, period, dtype_key=None, age=None):
<<<<<<< HEAD
        """
        Compiles operated area, given action code and period (and optionally list of development type keys or age).
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        aa = self.applied_actions
        acodes = [acode] if not self.actions[acode].components else self.actions[acode].components
        result = 0.
        for _acode in acodes:
            if not aa[period][_acode]: continue # acode not in solution
            dtype_keys = aa[period][_acode].keys() if dtype_key is None else [dtype_key]
            for _dtype_key in dtype_keys:
                ages = aa[period][_acode][_dtype_key].keys() if age is None else [age]
                for _age in ages:
                    result += aa[period][_acode][_dtype_key][_age][0]
        return result

    def repair_actions(self, period, areaselector=None):
        """
<<<<<<< HEAD
        Attempts to repair the action schedule for given period, using an AreaSelector object (defaults to class-default areaselector, which is a simple greedy oldest-first selector).
=======
        Attempts to repair the action schedule for given period.
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        """
        if areaselector is None: # use default (greedy) selector
            areaselector = self.areaselector
        aa = copy.copy(self.applied_actions[period])
        self.reset_actions(period)
        for acode in aa:
            if not aa[acode]: continue # null solution, move along...
            print ' ', acode
            old_area = 0.
            new_area = 0.
            # start by re-applying as much of the old solution as possible
            for dtype_key in aa[acode]:
                for age in aa[acode][dtype_key]:
                    aaa = aa[acode][dtype_key][age][0]
                    old_area += aaa
                    oa = self.dtypes[dtype_key].operable_area(acode, period, age)
                    if not oa: continue
                    applied_area = min(aaa, oa)
                    #print ' applying old area', applied_area
                    new_area += applied_area
                    self.apply_action(dtype_key, acode, period, age, applied_area)
            # try to make up for missing area...
            target_area = old_area - new_area
            print ' patched %i of %i solution hectares, missing' % (int(new_area), int(old_area)), target_area
            if areaselector is None: # use default area selector
                areaselector = self.areaselector
            areaselector.operate(period, acode, target_area)
                     
        
    def commit_actions(self, period=1, repair_future_actions=False, verbose=False):
<<<<<<< HEAD
        """
        Commits applied actions (i.e., apply transitions and grow, default starting at period 1).
        By default, will attempt to repair broken (infeasible) future actions, attempting to replace infeasiblea operated area using default AreaSelector.  
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        while period < self.horizon:
            if verbose: print 'growing period', period
            self.grow(period, cascade=False)
            period += 1
            if repair_future_actions:
                if verbose: print 'repairing actions in period', period
                self.repair_actions(period)
            else:
                self.reset_actions(period)
        
                                            
    def apply_action(self,
                     dtype_key,
                     acode,
                     period,
                     age,
                     area,
                     override_operability=False,
                     fuzzy_age=True,
                     recourse_enabled=True,
                     areaselector=None,
<<<<<<< HEAD
                     verbose=False):
        """
        Applies action, given action code, development type, period, age, area.
        Can optionally override operability limits, optionally use fuzzy age (i.e., attempt to apply action to proximal age class if specified age is not operable), optionally use default AreaSelector to patch missing area (if recourse enabled).
        Applying an action is a rather complex process, involving testing for operability (JIT-compiling operability expression as required), checking that valid transitions are defined, checking that area is available (possibly using fuzzy age and area selector functions to find missing area), generate list of target development types (from source development type and transition expressions [which may need to be JIT-compiled]), creating new development types (as needed), doing the area accounting correctly (without creating or destroying any area), and compiling the products from the action (which gets a bit complicated in the case of partial cuts...). 
        """
        assert area > 0 # stop wasting my time! :)
        if verbose > 1:
=======
                     verbose=False,
                     compile_sylv_cred=True,
                     compile_harv_cost=True):
        assert area > 0 # stop wasting my time! :)
        if verbose:# > 1:
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
            print 'applying action', [' '.join(dtype_key)], acode, period, age, area
        dt = self.dtypes[dtype_key]
        ############################################
        # TO DO: better error handling... ##########
        if acode not in dt.oper_expr:
            print 'requested action not defined for development type...'
            print ' ', [' '.join(dtype_key)], acode, period, age, area
            return
        if acode not in dt.operability: # action not compiled yet...
            if dt.compile_action(acode) == -1:
                print 'requested action is defined, but never not operable...'
                print ' ', [' '.join(dtype_key)], acode, period, age, area
                return
        if not dt.is_operable(acode, period, age) and not override_operability:
            print 'not operable'
            print ' '.join(dt.key), acode, period, age
            print dt.operability[acode][period]
            assert False # dt.is_operable(acode, period, age)
        if (acode, age) not in dt.transitions: # sanity check...
            print 'transitions not defined...'
            print ' ', [' '.join(dtype_key)], acode, period, age, area
            print dt.oper_expr
            print dt.operability
            print dt.transitions
            assert False 
            return
        if dt.area(period, age) - area < self.area_epsilon:
            # tweak area if slightly over or under, so we don't get any accounting drift...
            area = dt.area(period, age)            
        if dt.area(period, age) < area:
            # insufficient area in dt to operate (infeasible)
            # apply action to operable area, then look for missing area in adjacent ageclasses
            if dt.area(period, age) > 0: # operate available area before applying recourse
                self.apply_action(dtype_key, acode, period, age, dt.area(period, age),
                                  False, False, False, None, True)
            missing_area = area - dt.area(period, age)
            if fuzzy_age:
                for age_delta in [+1, -1, +2, -2]:
                    _age = age + age_delta
                    if dt.area(period, _age) > 0 and (acode, _age) in dt.transitions:
                        _area = min(missing_area, dt.area(period, _age))
                        self.apply_action(dtype_key, acode, period, _age, _area,
                                          False, False, False, None, True)
                        missing_area -= _area
                        if missing_area < self.area_epsilon: return
            if recourse_enabled:
                areaselector = self.areaselector if areaselector is None else areaselector
                missing_area = areaselector.operate(period, acode, missing_area)
                if missing_area < self.area_epsilon: return
            return missing_area
        action = self.actions[acode]
<<<<<<< HEAD

=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        #if not dt.actions[acode].is_compiled: dt.compile_action(acode)
        def resolve_replace(dtk, expr):
            # HACK ####################################################################
            # Too lazy to implement all the use cases.
            # This should work OK for BFEC models (TO DO: confirm).
            tokens = re.split('\s+', expr)
            i = int(tokens[0][3]) - 1
            try:
                return str(eval(expr.replace(tokens[0], dtk[i])))
            except:
                print 'source', ' '.join(dtype_key)
                print 'target', ' '.join(tmask), tprop, tage, tlock, treplace, tappend
                print 'dtk', ' '.join(dtk)
                raise
        ###########################################################################
        # HACK ####################################################################
        # Too lazy to implement.
        # Not used in BFEC models (TO DO: confirm).
        def resolve_append(dtk, expr):
            assert False # brick wall (deal with this case later, as needed)
        ###########################################################################
<<<<<<< HEAD
        dt.area(period, age, -area)
=======

        #print 'x', dtype_key, period, age, dt.area(period, age)
        dt.area(period, age, -area)
        #print 'x', dtype_key, period, age, dt.area(period, age)
        
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        target_dt = []
        for target in dt.transitions[acode, age]:
            tmask, tprop, tyield, tage, tlock, treplace, tappend = target # unpack tuple
            #print tmask
            dtk = list(dtype_key) # start with source key
            ###########################################################################
            # DO TO: Confirm correct order for evaluating mask, _APPEND and _REPLACE...
            dtk = [t if tmask[i] == '?' else tmask[i] for i, t in enumerate(dtk)] 
            if treplace: dtk[treplace[0]] = resolve_replace(dtk, treplace[1])
            if tappend: dtk[tappend[0]] = resolve_append(dtk, tappend[1])
            dtk = tuple(dtk)
            ###########################################################################
            foo = False
<<<<<<< HEAD
            #if acode in ['aca', 'acp']: foo = True 
            #print ' target mask', dtk
            if dtk not in self.dtypes: # new development type (clone source type)
                fookey = 'gs0062 forp 2 sr0053 fc0069 nat n inc zt0001 na na au2 na na env ev15 na tf5 utr9 na'
                if ' '.join(dtk) == fookey:
                    print 'fookey', tage, action.targetage, age
                    foo = 1
=======
            if dtk not in self.dtypes: # new development type (clone source type)
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
                self.create_dtype_fromkey(dtk)
            if tyield is not None: # yield-based age definition
                if foo:
                    print 'yield-based age definition', tyield, self.dt(dtk).ycomp(tyield[0]).lookup(tyield[1], roundx=True)
                try:
                    targetage = self.dt(dtk).ycomp(tyield[0]).lookup(tyield[1], roundx=True)
                except:
                    print ' '.join(dtk), tyield[0], self.dt(dtk).ycomps()
                    assert False
            elif tage is not None: # target age override specifed in transition
                if foo: print '_AGE override', tage
                targetage = tage
            elif action.targetage is None: # use source age
                if foo: print 'source age', age
                targetage = age
            else: # default: age reset to 0
                if foo: print 'default age reset to 0'
                targetage = 0
            if foo:
                print 'creating new dt from', acode, age, [' '.join(dt.key)]
                print ' new dt', [' '.join(dtk)], period, targetage, area, tprop, area*tprop
            self.dtypes[dtk].area(period, targetage, area*tprop)
            target_dt.append([dtk, tprop, targetage])

        aa = self.applied_actions[period][acode]
        if dtype_key not in aa: aa[dtype_key] = {}
        if age not in aa[dtype_key]: aa[dtype_key][age] = [0., {}] 
        aa[dtype_key][age][0] += area
        #if action.partial: # debug only
        #    print 'action.partial', acode, ' '.join(dtype_key) # action.partial
        #    target_dt = [self.dtypes[dtk] for dtk in target_dtk] # avoid multiple lookups in loop
        for yname in dt.ycomps():
            ycomp = dt.ycomp(yname)
            if ycomp.type in ['t', 'c']: continue # only track age-based ycomps for products
            if yname in action.partial:
                value = 0.
                for dtk, tprop, targetage in target_dt:
                    _dt = self.dtypes[dtk]
                    _value = 0.
                    if yname in dt.ycomps():
                        if yname in _dt.ycomps():
                            _value = (dt.ycomp(yname)[age] - _dt.ycomp(yname)[targetage])
                        else:
                            _value = dt.ycomp(yname)[age]
                    if _value > 0.:
                        value += _value * tprop
                    else:
                        if verbose:
                            if _value < 0:
                                print 'negative partial value', acode, yname, tprop, _value
                                print ' ', ''.join(dtype_key), age
                                print ' ', ''.join(dtk), targetage
                                print
            else: # not partial
                value = dt.ycomp(yname)[age]
            if value != 0.:
                aa[dtype_key][age][1][yname] = value
<<<<<<< HEAD

    def sylv_cred_formula(self, treatment_type, cover_type):
        """
        Select correct sylviculture credit formula, given treatment type and cover type.
        .. warning:: This only works for Quebec!
        """
=======
	return target_dt

    def sylv_cred_formula(self, treatment_type, cover_type):
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        if treatment_type == 'ec':
            return 1 if cover_type.lower() in ['r', 'm'] else 2
        if treatment_type == 'cj':
            return 4
        if treatment_type == 'cprog':
            return 7 if cover_type.lower() in ['r', 'm'] else 4        
        return 0

            
    def create_dtype_fromkey(self, key):
<<<<<<< HEAD
        """
        Creates a new development type, given a key (checks for existing, auto-assigns yield compompontents, auto-assign actions and transitions, checks for operability (filed under inoperable if applicable).
        """
        
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        assert key not in self.dtypes # should not be creating new dtypes from existing key
        dt = DevelopmentType(key, self)
        self.dtypes[key] = dt
        # assign yields
        for mask, t, ycomps in self.yields:
            if self.match_mask(mask, key):
                for yname, ycomp in ycomps:
                    dt.add_ycomp(t, yname, ycomp)
        # assign actions and transitions
        for acode in self.oper_expr:
            for mask in self.oper_expr[acode]:
                if self.match_mask(mask, key):
                    dt.oper_expr[acode].append(self.oper_expr[acode][mask]) 
            #print 'building transitions for acode', acode, ' '.join(key)
            for mask in self.transitions[acode]:
                #print ' mask', ' '.join(mask)
                #foo = False
                #if acode in ['acp']:
                    #if mask == tuple('gs0002 forestier 1 sr0087 ? nat o inc ? ? ? ? ? ? ? ? ? ? ? ?'.split(' ')):
                    #    print acode, ' '.join(mask) # DEBUG
                    #    foo = True
                if self.match_mask(mask, key):
                    #print '  match'
                    for scond in self.transitions[acode][mask]:
                        #print '   scond', scond, self.resolve_condition(scond, key)
                        #if foo:
                        #    print scond
                        #    print dt.ycomp('yg_s').points()
                        #    print self.resolve_condition(scond, key)
                        for x in self.resolve_condition(scond, key): 
                            #if foo:
                            #    print ' ', x
                            dt.transitions[acode, x] = self.transitions[acode][mask][scond]
        if not dt.transitions:
            self.inoperable_dtypes.append(key)
            #print 'no transitions', ' '.join(key)
            #for acode in self.transitions:
            #    for mask in self.transitions[acode]:
            #        for scond in self.transitions[acode][mask]:
            #            print acode, ' '.join(mask), scond
    
    def _resolve_outputs_buffer(self, s, for_flag=None):
        n = self.nthemes
        group = 'no_group' # outputs declared at top of file assigned to 'no_group'
        self.output_groups[group] = set()
        ocode = ''
        buffering_for = False
        s = re.sub(r'\{.*?\}', '', s, flags=re.M|re.S) # remove curly-bracket comments
        for l in re.split(r'[\r\n]+', s, flags=re.M|re.S):
            if re.match('^\s*(;|$)', l): continue # skip comments and blank lines
            matches = re.findall('#[A-Za-z0-9_]*', l)
            for m in matches: # replace CONSTANTS variables with value
                try:
                    l = l.replace(m, str(self.constants[m[1:].lower()]))
                except:
                    import sys
                    print sys.exc_info()[0]
                    print l
                    print matches, m
                    assert False

            if buffering_for:
                if l.strip().startswith('ENDFOR'):
                    for i in range(for_lo, for_hi+1):
                        ss = '\n'.join(for_buffer).replace(for_var, str(i))
                        self._resolve_outputs_buffer(ss, for_flag=i)
                    buffering_for = False
                    continue
                else:
                    for_buffer.append(l)
                    continue
            l = re.sub('\s+', ' ', l) # separate tokens by single space
            l = l.strip().partition(';')[0].strip()
            l = l.replace(' (', '(')  # remove space to left of left parentheses
            t = l.lower().split(' ')
            ##################################################
            # HACK ###########################################
            # substitute ugly symbols have in ocodes...
            l = l.replace(r'%', 'p')
            l = l.replace(r'$', 's')
            ##################################################
            tokens = l.lower().split(' ')
            if l.startswith('*GROUP'):
                keyword = 'group'
                group = tokens[1].lower()
                self.output_groups[group] = set()
            elif l.startswith('FOR'):
                # pattern matching may not be very robust, but works for now with:
                # 'FOR XX := 1 to 99'
                # TO DO: implement DOWNTO, etc.
                for_var = re.search(r'(?<=FOR\s).+(?=:=)', l).group(0).strip()
                for_lo = int(re.search(r'(?<=:=).+(?=to)', l).group(0))
                for_hi = int(re.search(r'(?<=to).+', l).group(0))
                for_buffer = []
                buffering_for = True
                continue
            if l.startswith('*OUTPUT') or l.startswith('*LEVEL'):
                keyword = 'output' if l.startswith('*OUTPUT') else 'level'
                if ocode: # flush data collected from previous lines
                    self.outputs[ocode] = Output(parent=self,
                                                 code=ocode,
                                                 expression=expression,
                                                 description=description,
                                                 theme_index=theme_index)
                tt = tokens[1].split('(')
                ocode = tt[0]
                theme_index = tt[1][3:-1] if len(tt) > 1 else None
                description = ' '.join(tokens[2:])
                expression = ''
                self.output_groups[group].add(ocode)
                if keyword == 'level':
                    self.outputs[ocode] = Output(parent=self,
                                                 code=ocode,
                                                 expression=expression,
                                                 description=description,
                                                 theme_index=theme_index,
                                                 is_level=True)
                    ocode = ''
            elif l.startswith('*SOURCE'):
                keyword = 'source'
                expression += l[8:]
            elif keyword == 'source': # continuation line of SOURCE expression
                expression += ' '
                expression += l       
        
    @timed
    def import_outputs_section(self, filename_suffix='out'):
<<<<<<< HEAD
        """
        Imports OUTPUTS section from a Woodstock model.
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        with open('%s/%s.%s' % (self.model_path, self.model_name, filename_suffix)) as f:
            s = f.read()
        self._resolve_outputs_buffer(s)
            
    @timed
    def import_landscape_section(self, filename_suffix='lan'):
<<<<<<< HEAD
        """
        Imports LANDSCAPE section from a Woodstock model.
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        with open('%s/%s.%s' % (self.model_path, self.model_name, filename_suffix)) as f:
            data = f.read()
        _data = re.search(r'\*THEME.*', data, re.M|re.S).group(0) # strip leading junk
        t_data = re.split(r'\*THEME.*\n', _data)[1:] # split into theme-wise chunks
        for ti, t in enumerate(t_data):
            self._themes.append({})
            self._theme_basecodes.append([])
            defining_aggregates = False
            for l in [l for l in t.split('\n') if not re.match('^\s*(;|{|$)', l)]: 
                if re.match('^\s*\*AGGREGATE', l): # aggregate theme attribute code
                    tac = re.split('\s+', l.strip())[1].lower()
                    self._themes[ti][tac] = []
                    defining_aggregates = True
                    continue
                if not defining_aggregates: # line defines basic theme attribute code
                    tac = re.search('\S+', l.strip()).group(0).lower()
                    self._themes[ti][tac] = tac
                    self._theme_basecodes[ti].append(tac)
                else: # line defines aggregate values (parse out multiple values before comment)
                    _tacs = [_tac.lower() for _tac in re.split('\s+', l.strip().partition(';')[0].strip())]
                    self._themes[ti][tac].extend(_tacs)
        self.nthemes = len(self._themes)

    def theme_basecodes(self, theme_index):
<<<<<<< HEAD
        """
        Return list of base codes, given theme index.
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        return self._themes[theme_index]
        
    @timed    
    def import_areas_section(self, filename_suffix='are', import_empty=False):
<<<<<<< HEAD
        """
        Imports AREAS section from a Woodstock model.
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        n = self.nthemes
        with open('%s/%s.%s' % (self.model_path, self.model_name, filename_suffix)) as f:
            for l in f:
                if re.match('^\s*(;|$)', l): continue # skip comments and blank lines
                l = l.lower().strip().partition(';')[0] # strip leading whitespace and trailing comments
                t = re.split('\s+', l)
                key = tuple(_t for _t in t[1:n+1])
<<<<<<< HEAD
=======
                #print t
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
                age = int(t[n+1])
                area = float(t[n+2].replace(',', ''))
                #print l[3:]
                #print 'foo'
                if area < self.area_epsilon and not import_empty: continue
                if key not in self.dtypes: self.dtypes[key] = DevelopmentType(key, self)
                self.dtypes[key].area(0, age, area)
                #if l[3:].startswith('gs0002 forestier 1 sr0084 fc0022 nat o inc zt0001 na m1 au1 b1 na orph ev17 na tf1 eco6 na'):
                #    print age, area, self.dt(key)._areas[0][age]
                #    assert False
                    
    def _expand_action(self, c):
        self._actions = t
        return [c] if t[c] == c else list(_cfi(self._expand_action(t, c) for c in t[c]))
                
    def _expand_theme(self, t, c, verbose=False): # depth-first search recursive aggregate theme code expansion
        if verbose:
            print t
            print c
        return [c] if t[c] == c else list(_cfi(self._expand_theme(t, c) for c in t[c]))

                
    def match_mask(self, mask, key):
        """
        Returns True if key matches mask.
        """
        #dt = self.dtypes[key]
        for ti, tac in enumerate(mask):
            if tac == '?': continue # wildcard matches all keys
            tacs = self._expand_theme(self._themes[ti], tac)
            if key[ti] not in tacs: return False # reject key
        return True # key matches
        
    def unmask(self, mask):
        """
        Iteratively filter list of development type keys using mask values.
        Accepts Woodstock-style string masks to facilitate cut-and-paste testing.
        """
        if isinstance(mask, str): # Woodstock string mask format
            mask = tuple(re.sub('\s+', ' ', mask).lower().split(' '))
            assert len(mask) == self.nthemes # must be bad mask if wrong theme count
        else:
            assert isinstance(mask, tuple) and len(mask) == self.nthemes
        dtype_keys = copy.copy(self.dtypes.keys()) # filter this
        for ti, tac in enumerate(mask):
            if tac == '?': continue # wildcard matches all
            tacs = self._expand_theme(self._themes[ti], tac)
            dtype_keys = [dtk for dtk in dtype_keys if dtk[ti] in tacs] # exclude bad matches
        return dtype_keys

    @timed                            
    def import_constants_section(self, filename_suffix='con'):
<<<<<<< HEAD
        """
        Imports CONSTANTS section from a Woodstock model.
        """

=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        with open('%s/%s.%s' % (self.model_path, self.model_name, filename_suffix)) as f:
            for lnum, l in enumerate(f):
                if re.match('^\s*(;|$)', l): continue # skip comments and blank lines
                l = l.strip().partition(';')[0].strip() # strip leading whitespace, trailing comments
                t = re.split('\s+', l)
                self.constants[t[0].lower()] = float(t[1])

    @timed        
    def import_yields_section(self, filename_suffix='yld', verbose=False):
<<<<<<< HEAD
        """
        Imports YIELDS section from a Woodstock model.
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        ###################################################
        # local utility functions #########################
        def flush_ycomps(t, m, n, c):
            #self.ycomps.update(n)
            if t == 'a': # age-based ycomps
                _c = lambda y: self.register_curve(core.Curve(y,
                                                              points=c[y],
                                                              type='a'))
                ycomps = [(y, _c(y)) for y in n]
            elif t == 't': # time-based ycomps (skimp on x range)
                _c = lambda y: self.register_curve(core.Curve(y,
                                                              points=c[y],
                                                              type='t',
                                                              xmax=self.horizon))
                ycomps = [(y, _c(y)) for y in n]
            else: # complex ycomps
                ycomps = [(y, c[y]) for y in n]
            self.yields.append((m, t, ycomps)) # stash for creating new dtypes at runtime...
            self.ynames.update(n)
            for k in self.unmask(m):
                for yname, ycomp in ycomps:
                    self.dtypes[k].add_ycomp(t, yname, ycomp)
        ###################################################
        n = self.nthemes
        ytype = ''
        mask = ('?',) * self.nthemes
        ynames = []
        data = None
        with open('%s/%s.%s' % (self.model_path, self.model_name, filename_suffix)) as f:
            for lnum, l in enumerate(f):
                if re.match('^\s*(;|$)', l): continue # skip comments and blank lines
                l = l.strip().partition(';')[0].strip() # strip leading whitespace and trailing comments
                t = re.split('\s+', l)
                if t[0].startswith('*Y'): # new yield definition
                    newyield = True
                    flush_ycomps(ytype, mask, ynames, data) # apply yield from previous block
                    ytype = self._ytypes[t[0]]
                    mask = tuple(_t.lower() for _t in t[1:])
                    if verbose: print lnum, ' '.join(mask)
                    continue
                if newyield:
                    if t[0] == '_AGE':
                        is_tabular = True
                        ynames = [_t.lower() for _t in t[1:]]
                        data = {yname:[] for yname in ynames}
                        newyield = False
                        continue
                    else:
                        is_tabular = False
                        ynames = []
                        data = {}
                        newyield = False
                else:
                    if t[0] == '_AGE': # same yield block, new table
                        flush_ycomps(ytype, mask, ynames, data) # apply yield from previous block
                        is_tabular = True
                        ynames = [_t.lower() for _t in t[1:]]
                        data = {yname:[] for yname in ynames}
                        newyield = False
                        continue
                if is_tabular:
                    try:
                        x = int(t[0])
                    except:
                        print lnum, l

                    for i, yname in enumerate(ynames):
                        data[yname].append((x, float(t[i+1])))
                else:
                    if ytype in 'at': # standard or time-based yield (extract xy values)
                        if not common.is_num(t[0]): # first line of row-based yield component
                            yname = t[0].lower()
                            ynames.append(yname)
                            data[yname] = [(i+int(t[1]), float(t[i+2])) for i in range(len(t)-2)]
                        else: # continuation of row-based yield compontent
                            x_last = data[yname][-1][0]
                            data[yname].extend([(i+x_last+1, float(t[i])) for i in range(len(t))])
                    else:
                        yname = t[0].lower()
                        ynames.append(yname)
                        data[yname] = t[1] # complex yield (defer interpretation) 
        flush_ycomps(ytype, mask, ynames, data)

    @timed        
    def import_actions_section(self, filename_suffix='act'):
<<<<<<< HEAD
        """
        Imports ACTIONS section from a Woodstock model.
        """

=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        n = self.nthemes
        actions = {}
        #oper = {}
        aggregates = {}
        partials = {}
        keyword = ''
        with open('%s/%s.%s' % (self.model_path, self.model_name, filename_suffix)) as f: s = f.read().lower()
        s = re.sub(r'\{.*?\}', '', s, flags=re.M|re.S) # remove curly-bracket comments
        for l in re.split(r'[\r\n]+', s, flags=re.M|re.S):
            if re.match('^\s*(;|$)', l): continue # skip comments and blank lines
            l = l.strip().partition(';')[0].strip() # strip leading whitespace and trailing comments
            l = re.sub('\s+', ' ', l) # separate tokens by single space
            tokens = l.split(' ')
            if l.startswith('*action'): 
                keyword = 'action'
                acode = tokens[1]
<<<<<<< HEAD
                targetage = 0 if tokens[2] == 'Y' else None
=======
                targetage = 0 if tokens[2] == 'y' else None
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
                descr = ' '.join(tokens[3:])
                lockexempt = '_lockexempt' in tokens
                self.actions[acode] = Action(acode, targetage, descr, lockexempt)
                self.oper_expr[acode] = {}
            elif l.startswith('*operable'):
                keyword = 'operable'
                acode = tokens[1]
            elif l.startswith('*aggregate'):
                keyword = 'aggregate'
                acode = tokens[1]
                self.actions[acode] = Action(acode)
            elif l.startswith('*partial'): 
                keyword = 'partial'
                acode = tokens[1]
                partials[acode] = []
            else: # continuation of OPERABLE, AGGREGATE, or PARTIAL block
                if keyword == 'operable':
                    self.oper_expr[acode][tuple(tokens[:n])] = ' '.join(tokens[n:])
                elif keyword == 'aggregate':
                    self.actions[acode].components.extend(tokens)
                elif keyword == 'partial':
                    self.actions[acode].partial.extend(tokens)
        for acode, a in self.actions.items():
            if a.components: continue # aggregate action, skip
            for mask, expression in self.oper_expr[acode].items():
                for k in self.unmask(mask):
                    #if acode == 'act1': print ' '.join(k), acode, expression
                    self.dtypes[k].oper_expr[acode].append(expression)

    def resolve_treplace(self, dt, treplace):
        if '_TH' in treplace: # assume incrementing integer theme value
            i = int(re.search('(?<=_TH)\w+', treplace).group(0))
            return eval(re.sub('_TH%i'%i, str(dt.key[i-1]), treplace))
        else:
            assert False # many other possible arguments (see Woodstock documentation)

    def resolve_tappend(self, dt, tappend):
        assert False # brick wall (not implemented yet)

    def resolve_tmask(self, dt, tmask, treplace, tappend):
<<<<<<< HEAD
        """
        Returns new developement type key (tuple of values, one per theme), given developement type and (treplace, tappend) expressions.
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        key = list(dt.key)
        if treplace:
            key[treplace[0]] = resolve_treplace(dt, treplace[1])
        if tappend:
            key[tappend[0]] = resolve_tappend(dt, tappend[1])
        for i, val in enumerate(tmask):
            if theme == '?': continue # wildcard (skip it)
            key[i] = val
        return tuple(key)

    def resolve_condition(self, condition, dtype_key=None):
        """
        Evaluate @AGE or @YLD condition.
        Returns list of ages.
        """
        if not condition:
            return self.ages
        elif condition.startswith('@AGE'):
            lo, hi = [int(a) for a in condition[5:-1].split('..')]
            return range(lo, hi+1)
        elif condition.startswith('@YLD'):
            args = re.split('\s?,\s?', condition[5:-1])
            yname = args[0].lower()
            lo, hi = [float(y) for y in args[1].split('..')]
            dt = self.dtypes[dtype_key]
            lo_age, hi_age = dt.ycomp(yname).range(lo, hi, as_bounds=True)
            return range(lo_age, hi_age+1)
            #return self.dtypes[dtype_key].resolve_condition(yname, hi, lo)
        
    @timed                        
    def import_transitions_section(self, filename_suffix='trn'):
<<<<<<< HEAD
        """
        Imports TRANSITIONS section from a Woodstock model.
        """
=======
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        # local utility function ####################################
        def flush_transitions(acode, sources):
            if not acode: return # nothing to flush on first loop
            self.transitions[acode] = {}
            for smask, scond in sources:
                #if acode in ['acp']:
                #    print [' '.join(smask)], scond, sources[smask, scond]
                # store transition data for future dtypes creation 
                if smask not in self.transitions[acode]:
                    self.transitions[acode][smask] = {}
                #if scond not in self.transitions[acode][smask]:
                #    self.transitions[acode][smask][scond] = []
                self.transitions[acode][smask][scond] = sources[smask, scond]
                # assign transitions to existing dtypes
                for k in self.unmask(smask):
                    dt = self.dtypes[k]
                    for x in self.resolve_condition(scond, k): # store targets
                        dt.transitions[acode, x] = sources[smask, scond] 
        # def flush_transitions(acode, sources):
        #     if not acode: return # nothing to flush on first loop
        #     for smask, scond in sources:
        #         for k in self.unmask(smask):
        #             dt = self.dtypes[k]
        #             for x in self.resolve_condition(scond, k): # store targets
        #                 dt.transitions[acode, x] = sources[smask, scond] 
        #############################################################                    
        acode = None
        with open('%s/%s.%s' % (self.model_path, self.model_name, filename_suffix)) as f:
            s = f.read()
        s = re.sub(r'\{.*?\}', '', s, flags=re.M|re.S) # remove curly-bracket comments
        for l in re.split(r'[\r\n]+', s, flags=re.M|re.S):
            if re.match('^\s*(;|$)', l): continue # skip comments and blank lines
            l = l.strip().partition(';')[0].strip() # strip leading whitespace, trailing comments
            tokens = re.split('\s+', l)
            if l.startswith('*CASE'):
                if acode: flush_transitions(acode, sources)
                acode = tokens[1].lower()
                sources = {}
            elif l.startswith('*SOURCE'):
                smask = tuple(t.lower() for t in tokens[1:self.nthemes+1])
                match = re.search(r'@.+\)', l)
                scond = match.group(0) if match else ''
                sources[(smask, scond)] = []
            elif l.startswith('*TARGET'):
                tmask = tuple(t.lower() for t in tokens[1:self.nthemes+1])
                tprop = float(tokens[self.nthemes+1]) * 0.01
                tyield = None
                if len(tokens) > self.nthemes+2 and tokens[self.nthemes+2].lower() in self.ynames:
                    tyield = (tokens[self.nthemes+2].lower(), float(tokens[self.nthemes+3]))
                #if len(tokens) > self.nthemes+2:
                #    print tokens[self.nthemes+2]
                #    if tokens[self.nthemes+2] in self.ynames:
                #        print 'tokens[self.nthemes+2]', tokens[self.nthemes+2]
                #        tyield = (tokens[self.nthemes+2], float(tokens[self.nthemes+3]))
                try: # _AGE keyword
                    tage = int(tokens[tokens.index('_AGE')+1])
                except:
                    tage = None
                try: # _LOCK keyword
                    tlock = int(tokens[tokens.index('_LOCK')+1])
                except:
                    tlock = None
                try: # _REPLACE keyword (TO DO: implement other cases)
                    args = re.split('\s?,\s?', re.search('(?<=_REPLACE\().*(?=\))', l).group(0))
                    theme_index = int(args[0][3]) - 1
                    treplace = theme_index, args[1]
                except:
                    treplace = None
                try: # _APPEND keyword (TO DO: implement other cases)
                    args = re.split('\s?,\s?', re.search('(?<=_APPEND\().*(?=\))', l).group(0))
                    theme_index = int(args[0][3]) - 1
                    tappend = theme_index, args[1]
                except:
                    tappend = None
                sources[(smask, scond)].append((tmask, tprop, tyield, tage, tlock, treplace, tappend))
        flush_transitions(acode, sources)

    
    def import_optimize_section(self, filename_suffix='opt'):
<<<<<<< HEAD
        """
        Imports OPTIMIZE section from a Woodstock model.
        .. warning:: Not implemented yet.
        """
        pass

    def import_graphics_section(self, filename_suffix='gra'):
        """
        Imports GRAPHICS section from a Woodstock model.
        .. warning:: Not implemented yet.

        """
        pass

    def import_lifespan_section(self, filename_suffix='lif'):
        """
        Imports LIFESPAN section from a Woodstock model.
        .. warning:: Not implemented yet.

        """
        pass


    def import_schedule_section(self, filename_suffix='seq', replace_commas=True, filename_prefix=None):
        """
        Imports SCHEDULE section from a Woodstock model.
        """
=======
        pass

    def import_graphics_section(self, filename_suffix='gra'):
        pass

    def import_lifespan_section(self, filename_suffix='lif'):
        pass

    def import_lifespan_section(self, filename_suffix='lif'):
        pass

    def import_schedule_section(self, filename_suffix='seq', replace_commas=True, filename_prefix=None):
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        filename_prefix = self.model_name if filename_prefix is None else filename_prefix
        schedule = []
        n = self.nthemes
        with open('%s/%s.%s' % (self.model_path, filename_prefix, filename_suffix)) as f:
            for lnum, l in enumerate(f):
                if re.match('^\s*(;|$)', l): continue # skip comments and blank lines
                l = l.lower().strip().partition(';')[0].strip() # strip leading whitespace and trailing comments
                t = re.split('\s+', l)
                if len(t) != n + 5: break
                dtype_key = tuple(t[:n])
                age = int(t[n])
                area = float(t[n+1].replace(',', '')) if replace_commas else float(t[n+1])
                acode = t[n+2]
                period = int(t[n+3])
                condition = t[n+4]
                schedule.append((dtype_key, age, area, acode, period, condition))
                if area <= 0: print 'area <= 0', l
        return schedule

    def apply_schedule(self, schedule, max_period=None, verbose=False):
        """
        Assumes schedule in format returned by import_schedule_section().
        That is: list of (dtype_key, age, area, acode, period, condition) tuples.
        Also assumes that actions in list are sorted by applied period.
        """
        if max_period is None: max_period = self.horizon
        self.reset_actions()
        self.initialize_areas()
        _period = 1
        for dtype_key, age, area, acode, period, condition in schedule:
            if period > _period:
                print 'apply_schedule: committing actions for period', _period
                self.commit_actions(_period)
            if period > max_period: return
            #print 'applying:', [' '.join(dtype_key)], age, area, acode, period, condition
            missing_area = self.apply_action(dtype_key,
                                             acode,
                                             period,
                                             age,
                                             area,
                                             override_operability=True,
                                             verbose=verbose)
            assert not missing_area 
            _period = period

    def import_control_section(self, filename_suffix='run'):
<<<<<<< HEAD
        """
        Imports CONTROL section from a Woodstock model.
        .. warning:: Not implemented yet.
        """
        pass

    def grow(self, start_period=1, cascade=True):
        """
        Simulates growth (default startint at period 1 and cascading to the end of the planning horizon).
        """
=======
        pass

    def grow(self, start_period=1, cascade=True):
>>>>>>> 68a12a6673e8e1ad13b9357329e005ad189c6644
        for dt in self.dtypes.values(): dt.grow(start_period, cascade)

if __name__ == '__main__':
    pass
