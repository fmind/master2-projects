package sm.applets;

import javacard.framework.*;

public class EchoApplet extends Applet {
	public static final byte MY_CLA = (byte)0x90;
	public static final byte INS_10 = (byte)0x10;
	public static final byte INS_20 = (byte)0x20;
	private byte[] RESP_10 = { (byte)0xAA, (byte)0xBB, (byte)0xCC };
	private byte[] RESP_20 = { (byte)0xDD, (byte)0xEE , (byte)0xFF };
	
	private EchoApplet() {
		register();
	}
	
	public static void install(byte[] byteArray, short offset, byte length) {
		new EchoApplet();
	}
	
	public void process(APDU apdu) {
		byte buffer[] = apdu.getBuffer();
		
		if (buffer[ISO7816.OFFSET_CLA] == MY_CLA) {
			switch (buffer[ISO7816.OFFSET_INS]){
			case INS_10:
				sendResponse(apdu, RESP_10);
				break;
			case INS_20:
				sendResponse(apdu, RESP_20);
				break;
			default:
				ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
			}
		}
	}
	
	protected void sendResponse(APDU apdu, byte[] respBytesData) {
		byte apduBuffer[] = apdu.getBuffer();
		Util.arrayCopy(respBytesData, (short)0, apduBuffer, (short)0, (short)respBytesData.length);
		short le = apdu.setOutgoing();
		apdu.setOutgoingLength(le);
		apdu.sendBytes( (short)0, le);
	}
}
