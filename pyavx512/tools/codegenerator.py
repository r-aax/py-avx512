import sem

# =================================================================================================================

def cg(f, ir):
    """
    Code generation.

    Parameters
    ----------
    f
        File.
    ir
        Intermediate representation.
    """

    f.write('{\n')

    for op in ir.CFG.Nodes[0].Opers:
        t = '' if op.PredctV else '~'
        if op.Name == 'fload':
            if op.Predct is None:
                f.write(f'\t{op.Res} = _mm512_load_ps(&{op.Args[0].Id}[i]);')
            else:
                raise Exception('NOT IMPLEMENTED')
        elif op.Name == 'fstore':
            if op.Predct is None:
                f.write(f'\t_mm512_store_ps(&{op.Args[1].Id}[i], {op.Args[0]});')
            else:
                f.write(f'\t_mm512_mask_store_ps(&{op.Args[1].Id}[i], {t}{op.Predct}, {op.Args[0]});')
        elif op.Name == 'fmov':
            if op.Predct is None:
                if op.Args[0].Kind == 'c':
                    f.write(f'\t{op.Args[1]} = _mm512_set1_ps({op.Args[0].Id});')
                else:
                    f.write(f'\t{op.Args[1]} = {op.Args[0]};')
        elif op.Name in ['fabs', 'fsqrt']:
            if op.Predct is None:
                f.write(f'\t{op.Res} = _mm512_{op.Name[1:]}_ps({op.Args[0]});')
            else:
                f.write(f'\t{op.Res} = _mm512_mask_{op.Name[1:]}_ps({op.Res}, {t}{op.Predct}, {op.Args[0]});')
        elif op.Name in ['fadd', 'fsub', 'fmul', 'fdiv', 'fmin', 'fmax', 'fpow']:
            if op.Predct is None:
                f.write(f'\t{op.Res} = _mm512_{op.Name[1:]}_ps({op.Args[0]}, {op.Args[1]});')
            else:
                f.write(f'\t{op.Res} = _mm512_mask_{op.Name[1:]}_ps({op.Res}, {t}{op.Predct}, {op.Args[0]}, {op.Args[1]});')
        elif op.Name in ['fcmpge', 'fcmpeq', 'fcmplt', 'fcmplte']:
            if op.Predct is None:
                f.write(f'\t{op.Res} = _mm512_{op.Name[1:]}_ps_mask({op.Args[0]}, {op.Args[1]})')
            else:
                f.write(f'\t{op.Res} = _mm512_mask_{op.Name[1:]}_ps_mask({op.Res}, {t}{op.Predct}, {op.Args[0]}, {op.Args[1]})')
        elif op.Name == 'pnot':
            f.write(f'\t{op.Res} = ~{op.Args[0]};')
        elif op.Name == 'pand':
            f.write(f'\t{op.Res} = {op.Args[0]} & {op.Args[1]};')
        elif op.Name == 'pandn':
            f.write(f'\t{op.Res} = {op.Args[0]} & ~{op.Args[1]};')
        elif op.Name == 'unary_minus':
            pass
        else:
            raise Exception(f'NOT IMPLEMENTED : {op.Name}')
        f.write('\n')

    f.write('}\n')

# =================================================================================================================
