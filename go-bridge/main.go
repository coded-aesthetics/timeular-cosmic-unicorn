package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/coded-aesthetics/bartolome-ble-toolkit/pkg/ble"
	"github.com/coded-aesthetics/bartolome-ble-toolkit/pkg/timeular"
)

const (
	// Update this with your Pico W's IP address
	PICO_W_IP = "192.168.0.185"
	
	// Timeular device name - update if needed
	TIMEULAR_NAME = "Timeular Tra"
	
	// Polling interval for faster response
	POLL_INTERVAL = 500 * time.Millisecond
)

func main() {
	fmt.Println("🎲 Timeular to Cosmic Unicorn Bridge")
	fmt.Println("====================================")
	fmt.Println("This bridge connects your Timeular tracker to a Cosmic Unicorn LED display.")
	fmt.Println("Rotate your Timeular device to see side changes in real-time on the LED matrix!")
	fmt.Println("")

	// Create a single Timeular device with custom configuration
	timeularDevice := timeular.NewDeviceWithConfig(timeular.Config{
		Name:         TIMEULAR_NAME,
		PollInterval: POLL_INTERVAL,
	})

	// Create a BLE manager
	manager := ble.NewManager()

	// Set up signal handling for graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	// Set up side change handler
	timeularDevice.OnSideChange(func(deviceName string, side byte) error {
		// Validate the side
		if !timeular.IsValidSide(side) {
			fmt.Printf("⚠️  Warning: Invalid side detected: %d\n", side)
			return fmt.Errorf("invalid side: %d", side)
		}

		// Determine color based on side (customize as needed)
		color := getColorForSide(side)
		
		// Build URL for Pico W server
		var picoURL string
		if color != "" {
			picoURL = fmt.Sprintf("http://%s/?num=%d&color=%s", PICO_W_IP, side, color)
		} else {
			picoURL = fmt.Sprintf("http://%s/?num=%d", PICO_W_IP, side)
		}

		fmt.Printf("🎲 Timeular side %d detected → Updating LED display (%s)\n", side, color)
		
		// Send HTTP request to Pico W
		response, err := http.Get(picoURL)
		if err != nil {
			fmt.Printf("❌ Error making request to Pico W: %v\n", err)
			fmt.Printf("   Make sure Pico W is running at %s\n", PICO_W_IP)
			return err
		}
		defer response.Body.Close()

		if response.StatusCode == 200 {
			fmt.Printf("✅ LED display updated successfully\n")
		} else {
			fmt.Printf("⚠️  Pico W returned status: %s\n", response.Status)
		}

		return nil
	})

	// Set up disconnect handler for robust reconnection
	manager.SetDisconnectHandler(func(deviceName, address string, err error) {
		fmt.Printf("⚠️  Device %s [%s] disconnected: %v\n", deviceName, address, err)
		fmt.Println("🔄 Will attempt to reconnect automatically...")
		// Reset device state
		timeularDevice.Reset()
	})

	// Configure device for BLE manager
	deviceConfig := ble.DeviceConfig{
		Name:               timeularDevice.GetName(),
		ServiceUUID:        timeularDevice.GetServiceUUID(),
		CharacteristicUUID: timeularDevice.GetCharacteristicUUID(),
		NotificationHandler: func(deviceName string, data []byte) error {
			return timeularDevice.ProcessNotification(deviceName, data)
		},
	}

	// Start connecting to device
	fmt.Printf("🔍 Searching for Timeular tracker: %s\n", timeularDevice.GetName())
	fmt.Println("📱 Make sure your Timeular device is turned on and nearby!")
	fmt.Printf("🖥️  Pico W server expected at: http://%s\n", PICO_W_IP)
	fmt.Println("")

	if err := manager.ConnectDevices([]ble.DeviceConfig{deviceConfig}); err != nil {
		log.Fatalf("❌ Failed to start device connection: %v", err)
	}

	fmt.Println("✅ Connection process started")
	fmt.Printf("🎲 Device supports %d sides (1-%d)\n", timeular.GetSupportedSides(), timeular.GetSupportedSides())
	fmt.Printf("⚡ Polling interval: %v\n", POLL_INTERVAL)
	fmt.Println("📝 Rotate your Timeular device to different sides!")
	fmt.Println("🛑 Press Ctrl+C to stop")
	fmt.Println("")

	// Wait for shutdown signal
	<-sigChan

	fmt.Println("\n🛑 Shutdown signal received...")

	// Stop the device
	fmt.Println("🛑 Stopping Timeular device...")
	timeularDevice.Stop()

	// Clean shutdown
	fmt.Println("🧹 Cleaning up BLE connections...")
	if err := manager.Close(); err != nil {
		fmt.Printf("⚠️  Error during shutdown: %v\n", err)
	}

	fmt.Println("👋 Thanks for using the Timeular to Cosmic Unicorn bridge!")
}

// getColorForSide returns a color string based on the Timeular side
// Customize this function to match your workflow
func getColorForSide(side byte) string {
	switch side {
	case 1, 2, 3:
		return "green" // Work/Focus time
	case 4, 5, 6:
		return "red"   // Break/Personal time
	case 7, 8:
		return "white" // Meetings/Other
	default:
		return "white" // Default color
	}
}
