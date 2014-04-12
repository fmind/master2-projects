package sm.appli;

import javax.smartcardio.*;

public class AppliClient1_ListTerminals {
	
	public static void main(String[] args) throws CardException {
		TerminalFactory defaultTermFactory = TerminalFactory.getDefault();
		CardTerminals terminalsList = defaultTermFactory.terminals();
		
		for (CardTerminal terminal : terminalsList.list()) {
			System.out.println(terminal.getName());
		}
	}
}
