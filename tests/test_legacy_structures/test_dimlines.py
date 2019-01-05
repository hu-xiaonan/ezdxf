# Copyright (c) 2018 Manfred Moitzi
# License: MIT License
import pytest
import ezdxf
from ezdxf.lldxf.const import DXFAttributeError
from ezdxf.render.dimension import format_text, DXFValueError


@pytest.fixture(scope='module')
def dxf12():
    dwg = ezdxf.new('R12', setup='all')
    return dwg


def test_dimstyle_standard_exist(dxf12):
    assert 'EZDXF' in dxf12.dimstyles


def test_dimstyle_override(dxf12):
    msp = dxf12.modelspace()
    dimline = msp.add_linear_dim(
        base=(3, 2, 0),
        ext1=(0, 0, 0),
        ext2=(3, 0, 0),
        dxfattribs={
            'dimstyle': 'EZDXF',
        }
    )
    assert dimline.dxf.dimstyle == 'EZDXF'

    preset = {
        'dimtxsty': 'TEST',
        'dimexe': 0.777,
    }
    dimstyle = dimline.dimstyle_override(preset)
    assert dimstyle['dimtxsty'] == 'TEST'
    assert dimstyle['dimexe'] == 0.777

    with pytest.raises(DXFAttributeError):
        _ = dimstyle['invalid']

    with pytest.raises(DXFAttributeError):
        dimstyle.update({'invalid': 0})

    dstyle_orig = dimstyle.get_dstyle_dict()
    assert len(dstyle_orig) == 0

    dimstyle.commit()
    dstyle = dimstyle.get_dstyle_dict()
    assert dstyle['dimexe'] == 0.777
    # unsupported DXF DimStyle attributes are not stored in dstyle
    assert 'dimtxsty' not in dstyle, 'dimtxsty is not a DXF12 attribute'


def test_horizontal_dimline(dxf12):
    msp = dxf12.modelspace()
    dimline = msp.add_linear_dim(
        base=(3, 2, 0),
        ext1=(0, 0, 0),
        ext2=(3, 0, 0),

    )
    assert dimline.dxf.dimstyle == 'EZDXF'

    msp.render_dimension(dimline)
    block_name = dimline.dxf.geometry
    assert block_name.startswith('*D')

    block = dxf12.blocks.get(block_name)
    assert len(list(block.query('TEXT'))) == 1
    assert len(list(block.query('LINE'))) == 5  # dimension line + 2 extension lines
    assert len(list(block.query('POINT'))) == 3  # def points


def test_format_text():
    assert format_text(0, dimrnd=0, dimdec=1, dimzin=0, dimpost='<>') == '0.0'
    assert format_text(0, dimrnd=0, dimdec=1, dimzin=4, dimpost='<>') == '0'
    assert format_text(0, dimrnd=0, dimdec=1, dimzin=8, dimpost='<>') == '0'
    assert format_text(1.23, dimrnd=0.5, dimdec=1, dimzin=0, dimpost='<> mm') == '1.0 mm'
    assert format_text(1.23, dimrnd=0.5, dimdec=1, dimzin=8, dimpost='<> mm') == '1 mm'
    assert format_text(1.23, dimrnd=0.5, dimdec=1, dimzin=12, dimpost='<> mm') == '1 mm'
    assert format_text(10.51, dimrnd=0.5, dimdec=2, dimzin=0, dimpost='<> mm') == '10.50 mm'
    assert format_text(10.51, dimrnd=0.5, dimdec=2, dimzin=8, dimpost='<> mm') == '10.5 mm'
    assert format_text(0.51, dimrnd=0.5, dimdec=2, dimzin=0, dimpost='mm <>') == 'mm 0.50'
    assert format_text(0.51, dimrnd=0.5, dimdec=2, dimzin=4, dimpost='mm <>') == 'mm .50'
    assert format_text(-0.51, dimrnd=0.5, dimdec=2, dimzin=4, dimpost='mm <>') == 'mm -.50'
    assert format_text(-0.11, dimrnd=0.1, dimdec=2, dimzin=4, dimpost='mm <>') == 'mm -.10'
    assert format_text(-0.51, dimdsep=',', dimpost='! <> m') == '! -0,51 m'

    assert format_text(-0.51, dimdsep=',', dimpost='') == '-0,51'
    assert format_text(-0.51, dimdsep=',', dimpost='<>') == '-0,51'
    assert format_text(-0.51, dimdsep=',', dimpost='><>') == '>-0,51'
    assert format_text(-0.51, dimdsep=',', dimpost='<><>') == '-0,51<>'  # ignore stupid
    with pytest.raises(DXFValueError):
        _ = format_text(-0.51, dimpost='<')
    assert format_text(-1.23, raisedec=True) == '-1²³'

