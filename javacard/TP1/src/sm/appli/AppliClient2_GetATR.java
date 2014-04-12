package sm.appli;

import javax.smartcardio.ATR;
import javax.smartcardio.Card;
import javax.smartcardio.CardException;
import javax.smartcardio.CardTerminal;
import javax.smartcardio.CardTerminals;
import javax.smartcardio.TerminalFactory;

public class AppliClient2_GetATR {
	
	/**
	 * Convert a byte[] array to readable Hex String format.
	 * @param in byte[] buffer to convert to string format
	 * @return result String buffer in String format
	 * 
	*/
	public static String fromBytesToHexString(byte inBytes[]) {
		StringBuffer buffer = new StringBuffer();
		
		for(int i=0;i<inBytes.length;i++) {
			// Get the first digit of the hexadecimal
			buffer.append(Integer.toHexString((inBytes[i] & 0xF0)>>4).toUpperCase());
			// Get the second digit of the hexadecimal
			buffer.append(Integer.toHexString(inBytes[i] & 0x0F).toUpperCase());
			// Append a blank space at the end of each hexadecimal
			buffer.append(" ");
		}
		
		return buffer.toString();
	}

	public static void main(String[] args) throws CardException {
		TerminalFactory factory = TerminalFactory.getDefault();
		CardTerminals terminals = factory.terminals();
		CardTerminal terminal = terminals.getTerminal("SCM Microsystems Inc. SCR33x USB Smart Card Reader 0");
		
		// attente de détection
		terminal.waitForCardPresent(15000);
		
		if (terminal.isCardPresent()) {
			System.out.println("Carte détectée");
			String CONNECTION_PROTOCOL = "*";
			
			// connexion à la carte
			Card insertedCard = terminal.connect(CONNECTION_PROTOCOL);
			
			// récupération de l'ATR
			ATR insertedCardATR = insertedCard.getATR();
			byte[] atrBytes = insertedCardATR.getBytes();
			
			// affichage de la longueur de l'ATR
			System.out.println(fromBytesToHexString(atrBytes));
		} else {
			System.out.println("Période expirée");
		}
	}
}
