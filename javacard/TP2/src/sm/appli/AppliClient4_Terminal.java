package sm.appli;

import javax.smartcardio.Card;
import javax.smartcardio.CardChannel;
import javax.smartcardio.CardException;
import javax.smartcardio.CardTerminal;
import javax.smartcardio.CardTerminals;
import javax.smartcardio.CommandAPDU;
import javax.smartcardio.ResponseAPDU;
import javax.smartcardio.TerminalFactory;

public class AppliClient4_Terminal {
	
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
		// sélection du lecteur de carte
		TerminalFactory factory = TerminalFactory.getDefault();
		CardTerminals terminals = factory.terminals();
		CardTerminal terminal = terminals.getTerminal("SCM Microsystems Inc. SCR33x USB Smart Card Reader 0");
		
		// attente: insertion de la carte
		terminal.waitForCardPresent(15000);
		
		// test: la carte est connectée ?
		if (terminal.isCardPresent()) {
			System.out.println("Carte détectée !");
			System.out.println("");
			
			// connexion à la carte
			String CONNECTION_PROTOCOL = "*";
			Card card = terminal.connect(CONNECTION_PROTOCOL);
			CardChannel channel = card.getBasicChannel();
			
			// sélection de l'applet
			byte[] data = {(byte) 0xEE, (byte) 0x00, (byte) 0x00, (byte) 0x00, (byte) 0x00, (byte) 0xBB};
			CommandAPDU cmd0 = new CommandAPDU(0x00, 0xA4, 0x04, 0x00, data, 0x02);
			ResponseAPDU response0 = channel.transmit(cmd0);
			System.out.println("Sélection de l'applet: " + fromBytesToHexString(cmd0.getBytes()) + " => " + fromBytesToHexString(response0.getBytes()));
			
			// création des requêtes
			CommandAPDU cmd1 = new CommandAPDU(0x90, 0x10, 0x0, 0x0, 0x03);
			CommandAPDU cmd2 = new CommandAPDU(0x90, 0x20, 0x0, 0x0, 0x03);

			// envoie des requêtes
			ResponseAPDU response1 = channel.transmit(cmd1);
			ResponseAPDU response2 = channel.transmit(cmd2);
			
			// affichage des réponses
			System.out.println("");
			System.out.println("CMD1: " + fromBytesToHexString(cmd1.getBytes()) + " => " + fromBytesToHexString(response1.getBytes()));
			System.out.println("CMD2: " + fromBytesToHexString(cmd2.getBytes()) + " => " + fromBytesToHexString(response2.getBytes()));
		
			// fermeture
			card.disconnect(true);
		} else {
			System.out.println("Timeout: aucune carte détectée");
		}
	}
}
