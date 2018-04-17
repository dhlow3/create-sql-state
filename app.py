"""Build GUI."""
from appJar import gui
from create_sql import parse_file
from os import path


if __name__ == '__main__':
    # Create GUI and set some properties
    app = gui('Create SQL Table')
    font = dict(size=10, family="Sans Serif", weight="normal")
    app.setFont(**font)

    # Add labels and entries
    app.addLabel('file_label', 'Select Data File to Process')
    app.addFileEntry('data_file')

    app.addLabel('n_label', 'Enter number of rows to parse')
    app.addNumericEntry('n')
    app.setEntryDefault('n', 'leave blank for all')

    app.addLabel('sep_label', 'Choose how the data is separated')
    app.addOptionBox('sep', ['tab', 'space', '|', ':', ',', ';'])

    app.addNamedCheckBox('Show commented data examples ', 'eg')

    # Button functions
    def copy_text(text):
        """Copy text to the clipboard."""
        app.topLevel.clipboard_append(text)

    def back():
        """Exit output window and return to main app."""
        app.topLevel.clipboard_clear()
        app.destroySubWindow("Output")
        app.show()

    def reset():
        """Define action for reset button."""
        app.clearAllEntries()
        app.clearOptionBox('sep')
        app.setCheckBox('eg', ticked=False)
        app.setFocus('data_file')

    def exit():
        """Define action for exit button."""
        app.stop()

    def process():
        """Define action for process button."""
        parse_args = app.getAllEntries()
        parse_args['sep'] = app.getOptionBox('sep')
        parse_args['eg'] = app.getCheckBox('eg')

        # Convert tab and space for processing
        if parse_args['sep'] == 'tab':
            parse_args['sep'] = '\t'
        elif parse_args['sep'] == 'space':
            parse_args['sep'] = ' '

        # Validate data_file and n entries
        invalid = False
        if not path.exists(parse_args['data_file']):
            app.errorBox('file_error', 'Invalid file')
            invalid = True

        if parse_args['n']:
            try:
                parse_args['n'] = int(parse_args['n'])
            except ValueError as e:
                app.errorBox('n_error', 'Invalid number of rows to parse')
                invalid = True

            if parse_args['n'] < 0:
                app.errorBox('n_error', 'Invalid number of rows to parse')
                invalid = True

        if not invalid:
            # If no error messages, output results to sub-window
            app.startSubWindow('Output', modal=True)

            try:
                # Do file parsing
                text = parse_file(parse_args)
            except Exception as e:
                app.stop()
                raise

            app.addLabel('result')
            app.setLabel('result', text)

            app.addButtons(['Back', 'Copy Text', 'Exit '],
                           [back, copy_text(text), exit])

            app.stopSubWindow()
            app.go(startWindow='Output')

    app.addButtons(['Process', 'Reset', 'Exit'], [process, reset, exit])

    app.go()
