__author__ = 'acuthbert'

from subprocess import check_output

UI_PYTHON_PATH = "../python/app/ui"


def build_ui(ui_name):
    print "Building UI: %s" % ui_name
    out = check_output(
        [
            'pyside-uic',
            '--from-imports',
            '%s.ui' % ui_name
        ]
    )
    amended_out = out.replace("from PySide import", "from tank.platform.qt import")

    with open("%s/%s.py" % (UI_PYTHON_PATH, ui_name), "w") as f:
        f.write(amended_out)


def build_res(res_name):
    print "Building Resource: %s" % res_name
    out = check_output(
        [
            "C:/Python27/Lib/site-packages/PySide/pyside-rcc",
            "%s.qrc" % res_name
        ]
    )
    with open("%s/%s_rc.py" % (UI_PYTHON_PATH, res_name), "w") as f:
        f.write(out)


if __name__ == "__main__":

    build_ui('dialog')
    # build_ui('asset_window')
    build_res('resources')